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

def generate_pattern(design: CyclographDesign) -> Pattern:
    pattern = []
    for t in np.linspace(0, 1, design.steps, endpoint=False):
        fixed_point = get_point_on_gear(design.fixed_gear, t)
        moving_center = fixed_point - get_point_on_gear(design.moving_gear, 0)
        rotation = 2 * np.pi * t * design.fixed_gear.sides / design.moving_gear.sides
        pen_point = moving_center + design.pen_distance * np.exp(1j * (rotation + design.pen_angle))
        pattern.append(pen_point)
    return Pattern(points=pattern, design=design)