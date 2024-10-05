from flask import Flask, jsonify, request, abort, send_file
from flask_cors import CORS
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import CyclographDesign, Pattern, Gear
from app.utils import generate_pattern, generate_regular_polygon, generate_line
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
    print("Received request to /api/generate")  # Debug print
    try:
        data = request.json
        print(f"Received data: {data}")  # Debug print
        design = convert_design_data(data)
        pattern = generate_pattern(design)
        return jsonify(pattern.to_dict())
    except ValueError as e:
        print(f"Error in generate: {str(e)}")  # Debug print
        abort(400, description=str(e))

@app.route('/api/gear/create', methods=['POST'])
def create_gear():
    print("Received request to /api/gear/create")  # Debug print
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
        print(f"Error in create_gear: {str(e)}")  # Debug print
        abort(400, description=str(e))

@app.route('/api/design/modify', methods=['PUT'])
def modify_design():
    print("Received request to /api/design/modify")  # Debug print
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
        print(f"Error in modify_design: {str(e)}")  # Debug print
        abort(400, description=str(e))

@app.route('/api/export/svg', methods=['POST'])
def export_svg():
    print("Received request to /api/export/svg")  # Debug print
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
        print(f"Error in export_svg: {str(e)}")  # Debug print
        abort(400, description=str(e))

@app.route('/api/export/png', methods=['POST'])
def export_png():
    print("Received request to /api/export/png")  # Debug print
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
        print(f"Error in export_png: {str(e)}")  # Debug print
        abort(400, description=str(e))

@app.route('/api/export/gcode', methods=['POST'])
def export_gcode():
    print("Received request to /api/export/gcode")  # Debug print
    try:
        data = request.json
        design = convert_design_data(data)
        pattern = generate_pattern(design)
        
        gcode = []
        gcode.append("G21 ; Set units to millimeters")
        gcode.append("G90 ; Use absolute coordinates")
        gcode.append("G0 Z5 ; Lift pen")
        
        for i, point in enumerate(pattern.points):
            x, y = point.real + 250, point.imag + 250
            if i == 0:
                gcode.append(f"G0 X{x:.3f} Y{y:.3f} ; Move to start position")
                gcode.append("G0 Z0 ; Lower pen")
            else:
                gcode.append(f"G1 X{x:.3f} Y{y:.3f} ; Draw line")
        
        gcode.append("G0 Z5 ; Lift pen")
        gcode.append("G0 X0 Y0 ; Return to origin")
        
        gcode_str = "\n".join(gcode)
        
        return gcode_str, 200, {'Content-Type': 'text/plain', 'Content-Disposition': 'attachment; filename=cyclograph.gcode'}
    except ValueError as e:
        print(f"Error in export_gcode: {str(e)}")  # Debug print
        abort(400, description=str(e))

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
    print("Starting Flask app...")  # Debug print
    app.run(debug=True, port=5001)
    print("Flask app has stopped.")  # Debug print