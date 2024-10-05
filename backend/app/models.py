from dataclasses import dataclass
from typing import List, Union

@dataclass
class Gear:
    shape: str  # 'polygon' or 'line'
    sides: int  # number of sides (2 for line)
    radius: float  # or length for line
    start_angle: float

@dataclass
class CyclographDesign:
    fixed_gear: Gear
    moving_gear: Gear
    pen_distance: float
    pen_angle: float
    path_type: str  # 'inside' or 'outside'
    line_movement: str  # 'along' or 'around', only for line fixed gear
    steps: int

@dataclass
class Pattern:
    points: List[complex]
    design: CyclographDesign

    def to_dict(self):
        return {
            'points': [(p.real, p.imag) for p in self.points],
            'design': self.design.__dict__
        }