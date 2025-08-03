#!/bin/bash
# Setup script for IP to Website Converter - Full Version
# This script sets up a virtual environment and installs all dependencies

echo "IP to Website Converter - Setup Script"
echo "======================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "Creating virtual environment..."
if python3 -m venv venv_ip_converter 2>/dev/null; then
    echo "✓ Virtual environment created"
else
    echo "Error: Could not create virtual environment"
    echo "On Debian/Ubuntu systems, you may need to install python3-venv:"
    echo "  sudo apt install python3-venv"
    exit 1
fi

# Activate virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source venv_ip_converter/bin/activate

if pip install -r requirements.txt; then
    echo "✓ Dependencies installed successfully"
else
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "Setup completed successfully!"
echo ""
echo "To use the full-featured version:"
echo "1. Activate the virtual environment:"
echo "   source venv_ip_converter/bin/activate"
echo ""
echo "2. Run the applications:"
echo "   python ip_to_website_cli.py 8.8.8.8"
echo "   python ip_to_website_gui.py"
echo ""
echo "3. Build executables:"
echo "   python build_executable.py"
echo ""
echo "To use the simple version (no setup required):"
echo "   python3 ip_to_website_simple.py 8.8.8.8"
echo ""
echo "Note: The simple version only provides basic hostname lookup."
echo "      The full version includes additional features like:"
echo "      - Organization and ISP information"
echo "      - Geographic location data"
echo "      - GUI interface"
echo "      - Executable building"