from flask import Flask, jsonify, request, abort, send_file
from flask_cors import CORS
import sys
import os
from io import BytesIO
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import CyclographDesign, Pattern, Gear
from app.utils import generate_pattern, generate_regular_polygon, generate_line, generate_gcode
import io
import svgwrite
from PIL import Image, ImageDraw
import numpy as np

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    return app

app = create_app()

@app.route('/api/generate', methods=['POST'])
def generate():
    logger.info("Received request to /api/generate")
    try:
        data = request.json
        logger.debug(f"Received data: {data}")
        
        # Extract path type (inside or outside) from the request, default to 'outside'
        path_type = data.get('path_type', 'outside')
        
        design = convert_design_data(data)
        pattern = generate_pattern(design, path_type=path_type)
        return jsonify(pattern.to_dict())
    except ValueError as e:
        logger.error(f"Error in generate: {str(e)}")
        abort(400, description=str(e))

@app.route('/api/gear/create', methods=['POST'])
def create_gear():
    logger.info("Received request to /api/gear/create")
    try:
        data = request.json
        gear = convert_gear_data(data)
        if gear.shape == 'polygon':
            points = generate_regular_polygon(gear.sides, gear.radius)
        elif gear.shape == 'line':
            points = generate_line(gear.radius)
        else:
            abort(400, description="Invalid gear shape")
        return jsonify({"points": points.tolist()})
    except ValueError as e:
        logger.error(f"Error in create_gear: {str(e)}")
        abort(400, description=str(e))

@app.route('/api/design/modify', methods=['PUT'])
def modify_design():
    logger.info("Received request to /api/design/modify")
    try:
        data = request.json
        design_id = data.pop('id', None)
        if design_id is None:
            abort(400, description="Design ID is required")
        # In a real application, you would fetch the design from a database
        # and update it. For now, we'll just create a new design.
        updated_design = convert_design_data(data)
        return jsonify(updated_design.__dict__)
    except ValueError as e:
        logger.error(f"Error in modify_design: {str(e)}")
        abort(400, description=str(e))

@app.route('/api/export/svg', methods=['POST'])
def export_svg():
    logger.info("Received request to /api/export/svg")
    try:
        data = request.json
        design = convert_design_data(data)
        pattern = generate_pattern(design)
        
        dwg = svgwrite.Drawing('cyclograph.svg', size=('100%', '100%'))
        dwg.viewbox(width=500, height=500)
        
        points = [(p.real + 250, p.imag + 250) for p in pattern.points]
        dwg.add(dwg.polyline(points=points, stroke='blue', fill='none'))
        
        svg_string = dwg.tostring()
        
        return send_file(
            io.BytesIO(svg_string.encode('utf-8')),
            mimetype='image/svg+xml',
            as_attachment=True,
            download_name='cyclograph.svg'
        )
    except ValueError as e:
        logger.error(f"Error in export_svg: {str(e)}")
        abort(400, description=str(e))

@app.route('/api/export/png', methods=['POST'])
def export_png():
    logger.info("Received request to /api/export/png")
    try:
        data = request.json
        design = convert_design_data(data)
        pattern = generate_pattern(design)
        
        img = Image.new('RGB', (500, 500), color='white')
        draw = ImageDraw.Draw(img)
        
        points = [(p.real + 250, p.imag + 250) for p in pattern.points]
        draw.line(points, fill='blue', width=1)
        
        img_io = io.BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='cyclograph.png')
    except ValueError as e:
        logger.error(f"Error in export_png: {str(e)}")
        abort(400, description=str(e))

@app.route('/api/export-gcode', methods=['POST'])
def export_gcode():
    logger.info("Received request to /api/export-gcode")
    try:
        data = request.json
        logger.debug(f"Received data for G-code export: {data}")

        # Extract design data
        design_data = data.get('design')
        if not design_data:
            raise ValueError("Design data is missing")

        # Convert design data to CyclographDesign object
        design = convert_design_data(design_data)
        logger.debug(f"Converted design: {design}")

        # Extract G-code options
        gcode_options = {
            "start_gcode": data.get("startGcode", "G90 ; use absolute positioning\nG21 ; use mm as unit\nG0 Z3 ; raise pen"),
            "end_gcode": data.get("endGcode", "G0 Z3 ; raise pen\nM2 ; end program"),
            "pen_down_command": data.get("penDownCommand", "G1 Z-1 F300 ; lower a bit slower"),
            "pen_up_command": data.get("penUpCommand", "G0 Z3"),
            "target_width": float(data.get("targetWidth", 200.0)),
            "target_height": float(data.get("targetHeight", 200.0)),
            "move_speed": int(data.get("moveSpeed", 1500)),
            "draw_speed": int(data.get("drawSpeed", 1000)),
            "starting_corner": data.get("startingCorner", '0,0'),
            "machine_rule": data.get("machineRule", 'right-hand')
        }
        logger.debug(f"G-code options: {gcode_options}")

        # Generate the pattern
        pattern = generate_pattern(design)
        logger.debug(f"Generated pattern with {len(pattern.points)} points")

        # Generate the G-code
        gcode_str = generate_gcode(pattern=pattern, **gcode_options)
        logger.debug(f"Generated G-code (first 100 chars): {gcode_str[:100]}...")

        # Prepare the G-code as a downloadable file
        gcode_bytes = BytesIO(gcode_str.encode('utf-8'))
        gcode_bytes.seek(0)

        return send_file(gcode_bytes, mimetype="text/plain", as_attachment=True, download_name="pattern.gcode")

    except Exception as e:
        logger.error(f"Error in export_gcode: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 400

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(500)
def server_error(e):
    return jsonify(error="An internal server error occurred"), 500

def convert_gear_data(gear_data):
    return Gear(
        shape=gear_data['shape'],
        sides=gear_data['sides'],
        radius=gear_data['radius'],
        start_angle=gear_data['startAngle']
    )

def convert_design_data(data):
    return CyclographDesign(
        fixed_gear=convert_gear_data(data['fixedGear']),
        moving_gear=convert_gear_data(data['movingGear']),
        pen_distance=data['penDistance'],
        pen_angle=data['penAngle'],
        path_type=data['pathType'],
        line_movement=data['lineMovement'],
        steps=data['steps']
    )

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5001))
    logger.info(f"Starting Flask app on port {port}...")
    app.run(debug=True, port=port)
    logger.info("Flask app has stopped.")