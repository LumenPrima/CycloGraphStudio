# Cyclograph Studio: Comprehensive Design Documents

## Table of Contents

1. Project Overview
2. Technology Stack
3. Architecture Design
4. User Interface Design
5. Core Algorithms
6. Data Models
7. Web Client Considerations
8. Performance Optimization
9. Testing Strategy
10. Deployment Plan
11. Future Enhancements

## 1. Project Overview

Cyclograph Studio is a web-based application for creating and manipulating spirograph-like patterns. It allows users to generate complex geometric designs using various shapes as gears, including regular polygons and lines. The application provides a rich, interactive interface for real-time pattern creation and editing.

### Key Features

- Custom gear shapes (regular polygons, lines)
- Real-time pattern preview
- Inside and outside rolling options
- Configurable starting points and pen positions
- SVG and raster image export
- G-code generation for CNC machines

## 2. Technology Stack

### Primary Technologies

- Language: Python 3.9+
- GUI Framework: PyQt 6
- Web Framework: Flask
- Frontend: HTML5, CSS3, JavaScript (React)
- Build Tool: PyInstaller (for desktop version)

### Key Libraries

- NumPy: For efficient numerical computations
- SciPy: For advanced mathematical functions
- Pillow: For image processing and export
- SVG.py: For SVG generation and manipulation

### Rationale

- Python: Offers rapid development, rich scientific libraries, and good performance with PyPy for computationally intensive tasks.
- PyQt: Provides a robust, cross-platform GUI framework with excellent performance and native look-and-feel.
- Flask: Lightweight web framework, easy to integrate with PyQt for web deployment.
- React: Enables creation of dynamic, responsive user interfaces for the web client.

## 3. Architecture Design

### High-Level Architecture

```plaintext
+-------------------+      +-------------------+
|    Web Client     |      |   Desktop Client  |
| (HTML/CSS/React)  |      |      (PyQt)       |
+--------+----------+      +---------+---------+
         |                           |
         |  HTTP/WebSocket           |
         |                           |
+--------v---------------------------v---------+
|               Flask Server                   |
|                                              |
|  +----------------+    +------------------+  |
|  | PyQt Core      |    | Pattern Generator |  |
|  | (Headless Mode)|    |                   |  |
|  +----------------+    +------------------+  |
|                                              |
|  +----------------+    +------------------+  |
|  | Data Models    |    | Export Modules   |  |
|  |                |    |                   |  |
|  +----------------+    +------------------+  |
+----------------------------------------------+
```

### Component Descriptions

1. Web Client: Provides the user interface for web browsers.
2. Desktop Client: Optional PyQt-based interface for desktop use.
3. Flask Server: Handles HTTP requests and WebSocket connections.
4. PyQt Core: Manages the application logic and state.
5. Pattern Generator: Implements the core algorithms for pattern creation.
6. Data Models: Defines the structure for storing and manipulating pattern data.
7. Export Modules: Handles exporting patterns to various formats (SVG, PNG, G-code).

## 4. User Interface Design

### Web Client Layout

```plaintext
+--------------------------------------------------+
|                  Header / Menu                   |
+--------------------------------------------------+
|   Controls Panel   |                             |
|                    |                             |
|  +---------------+ |                             |
|  | Fixed Gear    | |                             |
|  +---------------+ |                             |
|  | Moving Gear   | |         Pattern             |
|  +---------------+ |         Preview             |
|  | Path Config   | |          Area               |
|  +---------------+ |                             |
|  | Pen Config    | |                             |
|  +---------------+ |                             |
|  | Animation     | |                             |
|  +---------------+ |                             |
|                    |                             |
+--------------------+-----------------------------+
|               Export / Save Options              |
+--------------------------------------------------+
```

### Key UI Components

1. Fixed Gear Control:

   ```plaintext
   +---------------Fixed Gear------------------+
   | Shape:    [Dropdown: Line, Triangle, ...  ] |
   | Size:     [Slider-------------------------] |
   |           [   Text Box   ] [px]            |
   | Start At: [Angle Input] [Vertex Dropdown] |
   +---------------------------------------------+
   ```

2. Moving Gear Control:

   ```plaintext
   +---------------Moving Gear-----------------+
   | Shape:    [Dropdown: Triangle to 100-gon ] |
   | Size:     [Slider-------------------------] |
   |           [   Text Box   ] [px]            |
   | Start At: [Angle Input] [Vertex Dropdown] |
   +---------------------------------------------+
   ```

3. Path Configuration:

   ```plaintext
   +---------------Path Config------------------+
   | Type:     [Radio: Outside | Inside       ] |
   | Line Movement: [Dropdown: Along | Around  ] |
   +---------------------------------------------+
   ```

4. Pen Configuration:

   ```plaintext
   +---------------Pen Config-------------------+
   | Distance: [Slider-------------------------] |
   |           [   Text Box   ] [px]            |
   | Angle:    [Slider-------------------------] |
   |           [   Text Box   ] [degrees]       |
   +---------------------------------------------+
   ```

5. Animation Controls:

   ```plaintext
   +---------------Animation--------------------+
   | [Play] [Pause] [Reset]                     |
   | Speed:   [Slider-------------------------] |
   |           [   Text Box   ] [steps/s]       |
   +---------------------------------------------+
   ```

### Responsive Design

- Use CSS Grid and Flexbox for flexible layout
- Implement breakpoints for different screen sizes
- Collapse control panel into a sidebar on mobile devices

## 5. Core Algorithms

### 5.1 Regular Polygon Generation

```python
import numpy as np

def generate_regular_polygon(sides, radius):
    angles = np.linspace(0, 2 * np.pi, sides, endpoint=False)
    return radius * np.exp(1j * angles)

def get_point_on_polygon(polygon, t):
    n = len(polygon)
    index = int(t * n)
    next_index = (index + 1) % n
    frac = t * n - index
    return polygon[index] * (1 - frac) + polygon[next_index] * frac
```

### 5.2 Line as Fixed Gear

```python
def generate_line(length):
    return np.array([0, length])

def get_point_on_line(line, t):
    return line[0] * (1 - t) + line[1] * t
```

### 5.3 Pattern Generation

```python
def generate_pattern(fixed_gear, moving_gear, pen_distance, pen_angle, steps):
    pattern = []
    for t in np.linspace(0, 1, steps, endpoint=False):
        fixed_point = get_point_on_gear(fixed_gear, t)
        moving_center = fixed_point - get_point_on_gear(moving_gear, 0)
        rotation = 2 * np.pi * t * len(fixed_gear) / len(moving_gear)
        pen_point = moving_center + pen_distance * np.exp(1j * (rotation + pen_angle))
        pattern.append(pen_point)
    return np.array(pattern)
```

## 6. Data Models

### 6.1 Gear Model

```python
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
```

## 7. Web Client Considerations

### 7.1 Client-Server Communication

- Use WebSocket for real-time updates
- Implement REST API for static data and configuration

### 7.2 State Management

- Use Redux for global state management
- Implement local component state for UI-specific data

### 7.3 Rendering

- Use HTML5 Canvas for pattern rendering
- Implement WebGL for complex or large patterns

### 7.4 Offline Capabilities

- Use Service Workers for offline access
- Implement local storage for saving designs

## 8. Performance Optimization

### 8.1 Computation Optimization

- Use NumPy for vectorized calculations
- Implement caching for frequently used calculations

### 8.2 Rendering Optimization

- Implement level-of-detail rendering for large patterns
- Use Web Workers for background calculations

### 8.3 Network Optimization

- Implement data compression for WebSocket communication
- Use CDN for static assets

## 9. Testing Strategy

### 9.1 Unit Testing

- Use pytest for Python unit tests
- Implement Jest for JavaScript unit tests

### 9.2 Integration Testing

- Use Selenium for end-to-end testing
- Implement API testing using pytest-flask

### 9.3 Performance Testing

- Use locust for load testing
- Implement browser performance profiling

## 10. Deployment Plan

### 10.1 Server Deployment

- Use Docker for containerization
- Implement Kubernetes for orchestration

### 10.2 Client Deployment

- Use Webpack for bundling and optimization
- Implement CDN for static asset delivery

### 10.3 Continuous Integration/Continuous Deployment (CI/CD)

- Use GitHub Actions for automated testing and deployment
- Implement staged rollouts for new features

## 11. Future Enhancements

### 11.1 Advanced Features

- Support for custom, user-defined gear shapes
- Implement 3D spirograph patterns
- Add support for multiple pen points

### 11.2 Collaboration Features

- Implement real-time collaboration on designs
- Add a gallery for sharing and discovering patterns

### 11.3 Machine Learning Integration

- Implement pattern recognition for recreating physical spirograph designs
- Use AI for suggesting design improvements or variations

### 11.4 Mobile App Development

- Develop native mobile apps for iOS and Android
- Implement touch-optimized controls for mobile interfaces

This comprehensive design document provides a solid foundation for the development of Cyclograph Studio. It covers the key aspects of the project, from high-level architecture to specific algorithms and future enhancements. As development progresses, this document should be regularly updated to reflect new decisions and changes in the project scope.
