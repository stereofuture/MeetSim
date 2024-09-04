#!/bin/bash

# Step 1: Create .vscode directory
mkdir -p .vscode
echo "Created .vscode directory."

# Step 2: Create launch.json file
cat > .vscode/launch.json <<EOL
{
    "version": "0.2.0",
    "configurations": [
            {
            "name": "Python: Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "${file}"
            ],
        },
    ]
}
EOL
echo "Created launch.json with Python debug configuration."
