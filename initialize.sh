#!/bin/sh

if [ ! -d "env" ]; then
    echo "Creating virtual environment: env"
    python3 -m venv env
    source env/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "Done!"
fi