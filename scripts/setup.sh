#!/bin/bash
# Setup script for LinkedIn-Jekyll Cross-Posting Automation

echo "Setting up LinkedIn-Jekyll Cross-Posting Automation..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the cross-poster:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Copy and configure your credentials:"
echo "     cp .env.example .env"
echo "     # Then edit .env with your LinkedIn credentials"
echo ""
echo "  3. Run the cross-poster:"
echo "     python cross_poster.py --help"
echo ""
echo "To deactivate the virtual environment when done:"
echo "  deactivate"
echo ""
