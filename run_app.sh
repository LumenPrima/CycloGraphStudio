#!/bin/bash

set -e

# Navigate to the backend directory
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "cyclograph_env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv cyclograph_env
fi

# Activate the virtual environment
source cyclograph_env/bin/activate

# Upgrade pip and install requirements
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Set the Flask port
export FLASK_PORT=5001

# Start the backend Flask server
echo "Starting Flask app..."
python app/main.py &

# Navigate to the frontend directory
cd ../frontend

# Install frontend dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start the frontend React development server
echo "Starting React app..."
npm start

# Wait for both processes to finish
wait