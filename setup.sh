#!/bin/bash

# Step 1: Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# Step 2: Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Step 3: Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Step 4: Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found, skipping dependency installation."
fi

# Step 5: Run pytest to verify the setup
echo "Running pytest to verify the setup..."
pytest

# Step 6: Deactivate the virtual environment
echo "Deactivating virtual environment..."
deactivate

echo "Setup complete!"

