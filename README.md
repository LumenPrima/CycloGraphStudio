# Cyclograph Studio

Cyclograph Studio is a web application for creating and manipulating cyclic graphs.

## Setup

### Prerequisites

- Python 3.12 or higher
- Node.js and npm

### Backend Setup

1. Create a virtual environment:
   ```
   python3 -m venv cyclograph_env
   ```

2. Activate the virtual environment:
   ```
   source cyclograph_env/bin/activate
   ```

3. Install the required Python packages:
   ```
   pip install Flask numpy scipy Pillow svgwrite
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd cyclograph_studio/frontend
   ```

2. Install the required Node.js packages:
   ```
   npm install
   ```

## Running the Application

To run both the backend and frontend servers simultaneously, use the provided script:

```
./run_app.sh
```

This script will:
1. Start the backend server
2. Start the frontend development server

The application should now be accessible at `http://localhost:3000`.

## Development

- Backend code is located in the `cyclograph_studio/backend` directory.
- Frontend code is located in the `cyclograph_studio/frontend` directory.

## Troubleshooting

If you encounter any issues while setting up or running the application, please check the following:

1. Ensure that you have the correct versions of Python and Node.js installed.
2. Make sure all dependencies are correctly installed for both backend and frontend.
3. Check that the virtual environment is activated when running the backend.

For more detailed error messages, you can run the backend and frontend servers separately:

- Backend: `python cyclograph_studio/backend/app/main.py`
- Frontend: `cd cyclograph_studio/frontend && npm start`

If problems persist, please refer to the error messages and consult the project documentation or seek assistance from the development team.
