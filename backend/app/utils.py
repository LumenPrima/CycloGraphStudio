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

