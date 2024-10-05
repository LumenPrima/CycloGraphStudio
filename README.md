# Cyclograph Studio

Cyclograph Studio is a web application for creating and manipulating cyclic graphs.

**Note: Currently, the shapes are not yet generating correctly. This issue is being addressed.**

## Project Structure

The project is organized into backend and frontend directories:

- `backend/`: Contains the Flask server and Python logic
- `frontend/`: Contains the React application

## Setup

### Prerequisites

- Python 3.12 or higher
- Node.js and npm

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
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

- Backend code is located in the `backend/app/` directory.
- Frontend code is located in the `frontend/src/` directory.
- Main components:
  - `backend/app/main.py`: Flask server setup
  - `backend/app/models.py`: Data models
  - `backend/app/utils.py`: Utility functions
  - `frontend/src/App.js`: Main React component
  - `frontend/src/components/`: React components for different parts of the UI

## Testing

Tests are located in the `tests/` directory. (Note: Implement tests as the project progresses)

## Troubleshooting

If you encounter any issues while setting up or running the application, please check the following:

1. Ensure that you have the correct versions of Python and Node.js installed.
2. Make sure all dependencies are correctly installed for both backend and frontend.
3. Check that you're in the correct directory when running commands.

For more detailed error messages, you can run the backend and frontend servers separately:

- Backend: `python backend/app/main.py`
- Frontend: `cd frontend && npm start`

If problems persist, please refer to the error messages and consult the project documentation or seek assistance from the development team.

## Known Issues

- The shapes are not yet generating correctly. This is a known issue that is currently being worked on.

## Next Steps

- Implement correct shape generation
- Add more customization options for cyclic graphs
- Improve error handling and user feedback
- Implement comprehensive testing suite
