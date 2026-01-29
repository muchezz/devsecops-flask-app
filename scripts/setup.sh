#!/bin/bash

# DevSecOps Flask Application Setup Script
# Quickly set up the development environment

set -e

echo "=========================================="
echo "DevSecOps Flask App Setup"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.9"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then 
    echo -e "${GREEN}✓ Python $python_version detected${NC}"
else
    echo "✗ Python 3.9+ required"
    exit 1
fi
echo ""

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment created${NC}"
echo ""

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip
echo -e "${GREEN}✓ Pip upgraded${NC}"
echo ""

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt
pip install -r requirements-dev.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Install security tools
echo -e "${YELLOW}Installing security tools...${NC}"
pip install bandit safety semgrep
echo -e "${GREEN}✓ Security tools installed${NC}"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cat > .env << EOF
FLASK_ENV=development
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
JWT_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
DATABASE_URL=sqlite:///app.db
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi
echo ""

# Initialize database
echo -e "${YELLOW}Initializing database...${NC}"
python3 << EOF
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
print("Database initialized")
EOF
echo -e "${GREEN}✓ Database initialized${NC}"
echo ""

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
pytest tests/ -v
echo -e "${GREEN}✓ Tests passed${NC}"
echo ""

echo "=========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Quick Start:"
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the application:"
echo "     python run.py"
echo ""
echo "  3. Run security scans:"
echo "     ./scripts/run-security-scan.sh"
echo ""
echo "  4. Run tests:"
echo "     pytest tests/ -v"
echo ""
echo "  5. Access the app:"
echo "     http://localhost:5000"
echo ""
echo "Documentation:"
echo "  - README.md - Project overview"
echo "  - SECURITY.md - Security policy"
echo "  - docs/ - Additional documentation"
echo ""
