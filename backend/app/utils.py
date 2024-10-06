import numpy as np
from app.models import Gear, CyclographDesign, Pattern

def generate_regular_polygon(sides, radius):
    angles = np.linspace(0, 2 * np.pi, sides, endpoint=False)
    return radius * np.exp(1j * angles)

def generate_line(length):
    return np.array([0, length])

def get_point_on_gear(gear: Gear, t: float) -> complex:
    if gear.shape == 'polygon':
        polygon = generate_regular_polygon(gear.sides, gear.radius)
        n = len(polygon)
        index = int(t * n)
        next_index = (index + 1) % n
        frac = t * n - index
        return polygon[index] * (1 - frac) + polygon[next_index] * frac
    elif gear.shape == 'line':
        line = generate_line(gear.radius)
        return line[0] * (1 - t) + line[1] * t
    else:
        raise ValueError(f"Unknown gear shape: {gear.shape}")

def generate_pattern(design: CyclographDesign, path_type: str = 'outside') -> Pattern:
    pattern = []
    
    # Increase steps for smoother patterns
    steps = max(design.steps, 500)
    
    # Calculate the perimeters (approximation for polygons)
    perimeter_fixed = design.fixed_gear.sides * design.fixed_gear.radius
    perimeter_moving = design.moving_gear.sides * design.moving_gear.radius
    
    # Perimeter ratio for rolling without slipping
    perimeter_ratio = perimeter_fixed / perimeter_moving
    
    # Set tracing direction based on path type (inside or outside)
    reverse_rotation = -1 if path_type == 'inside' else 1

    for t in np.linspace(0, 1, steps, endpoint=False):
        # Get the position of the moving gear as it rolls along the fixed gear's edge
        fixed_point = get_point_on_gear(design.fixed_gear, t)
        
        # Calculate the arc length traveled by the moving shape along the fixed shape
        arc_length = t * perimeter_fixed
        
        # Calculate the rotation of the moving shape based on the perimeter ratio and path type
        rotation = reverse_rotation * arc_length * perimeter_ratio
        
        # Calculate the center of the moving shape relative to the fixed point
        if path_type == 'inside':
            # For inside tracing, the moving shape's center is inside the fixed shape
            moving_center = fixed_point + get_point_on_gear(design.moving_gear, 0)
        else:
            # For outside tracing, the moving shape's center is outside the fixed shape
            moving_center = fixed_point - get_point_on_gear(design.moving_gear, 0)
        
        # Pen point relative to the moving shape
        pen_point = moving_center + design.pen_distance * np.exp(1j * (rotation + design.pen_angle))
        
        # Trace the pen's path
        pattern.append(pen_point)
    
    # Convert to Pattern object
    return Pattern(points=pattern, design=design)

def generate_gcode(
    pattern,
    start_gcode="G90 ; use absolute positioning\nG21 ; use mm as unit\nG0 Z3 ; raise pen",
    end_gcode="G0 Z3 ; raise pen\nM2 ; end program",
    pen_down_command="G1 Z-1 F300 ; lower a bit slower",
    pen_up_command="G0 Z3",
    target_width=200,
    target_height=200,
    move_speed=1500,
    draw_speed=1000,
    starting_corner='0,0',
    machine_rule='right-hand'
):
    """
    Generates G-code for the given pattern with customizable start/end blocks,
    scaling, machine rule adjustments, and corner offset to keep coordinates positive.
    """
    gcode = []

    # Append the start G-code block
    gcode.append(start_gcode)

    # Initialize the starting position
    gcode.append(f"G0 F{move_speed} ; Set move speed")

    # Calculate the bounding box of the pattern
    min_x = min(p.real for p in pattern.points)
    max_x = max(p.real for p in pattern.points)
    min_y = min(p.imag for p in pattern.points)
    max_y = max(p.imag for p in pattern.points)

    # Calculate the width and height of the bounding box
    pattern_width = max_x - min_x
    pattern_height = max_y - min_y

    # Calculate scaling factor to fit within target width/height
    scale_x = target_width / pattern_width
    scale_y = target_height / pattern_height
    scale = min(scale_x, scale_y)  # Keep aspect ratio

    # Offset to ensure positive coordinates
    if starting_corner == '0,0':
        offset_x = -min_x * scale
        offset_y = -min_y * scale
    else:  # If user wants top-right or other options, customize here
        offset_x = target_width - (max_x * scale)
        offset_y = target_height - (max_y * scale)

    # Apply transformation based on the machine rule (right-hand or left-hand)
    if machine_rule == 'left-hand':
        scaled_points = [
            (-p.real * scale + offset_x, p.imag * scale + offset_y) for p in pattern.points
        ]
    else:  # Default right-hand rule
        scaled_points = [
            (p.real * scale + offset_x, p.imag * scale + offset_y) for p in pattern.points
        ]

    # Move to the starting point without drawing
    start_point = scaled_points[0]
    gcode.append(f"G0 X{start_point[0]:.3f} Y{start_point[1]:.3f} ; Move to start")

    # Pen down with feed rate reset
    gcode.append(pen_down_command)
    gcode.append(f"G1 F{draw_speed} ; Set drawing speed")

    # Draw the pattern
    for x, y in scaled_points[1:]:
        gcode.append(f"G1 X{x:.3f} Y{y:.3f} ; Drawing point")

    # Pen up with feed rate reset
    gcode.append(pen_up_command)
    gcode.append(f"G1 F{draw_speed} ; Reset drawing speed after pen up")

    # Append the end G-code block
    gcode.append(end_gcode)

    # Combine all the G-code lines into a single string
    return "\n".join(gcode)

