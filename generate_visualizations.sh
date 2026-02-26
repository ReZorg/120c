#!/usr/bin/env bash
# Run the 120-Cell Egregore visualization script

set -e

echo "120-Cell Egregore Visualization Generator"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
python3 -c "import numpy, matplotlib, scipy" 2>/dev/null || {
    echo "Installing required dependencies..."
    pip install -r requirements.txt
}

# Run the visualization script
echo ""
echo "Generating visualizations..."
python3 src/visualization/visualize_120cell_egregore.py

echo ""
echo "Done! Check docs/images/ for the generated visualizations."
