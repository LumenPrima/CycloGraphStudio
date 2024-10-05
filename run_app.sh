#!/bin/bash

# Activate the existing virtual environment
cd backend
source cyclograph_env/bin/activate

# Upgrade pip and install Flask-CORS separately
pip install --upgrade pip
pip install Flask-CORS==4.0.0

# Install the rest of the requirements
pip install -r requirements.txt

# Start the backend Flask server
python app/main.py &

# Start the frontend React development server
cd ../frontend
npm start

# Wait for both processes to finish
wait