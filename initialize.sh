#!/bin/sh

if [ ! -d "env" ]; then
    echo "Creating virtual environment: env"
    python3 -m venv env
    source env/bin/activate
    echo "Upgrading pip..."
    python3 -m pip install --upgrade pip
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "Installing pre-commit hooks..."
    pre-commit install
    echo "Done!"
fi