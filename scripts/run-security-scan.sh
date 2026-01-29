#!/bin/bash

# DevSecOps Local Security Scan Script
# Run all security scans locally before pushing to GitHub

set -e

echo "=========================================="
echo "DevSecOps Security Scan Pipeline"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create reports directory
mkdir -p reports

# 1. Secret Scanning
echo -e "${YELLOW}[1/7] Running Secret Detection...${NC}"
if command -v gitleaks &> /dev/null; then
    gitleaks detect --source . --report-path reports/gitleaks-report.json --verbose || true
    echo -e "${GREEN}✓ Secret scan completed${NC}"
else
    echo -e "${RED}✗ GitLeaks not installed. Install: https://github.com/gitleaks/gitleaks${NC}"
fi
echo ""

# 2. Dependency Scanning
echo -e "${YELLOW}[2/7] Running Dependency Vulnerability Scan...${NC}"
if command -v safety &> /dev/null; then
    safety check --json --output reports/safety-report.json || true
    echo -e "${GREEN}✓ Dependency scan completed${NC}"
else
    echo -e "${RED}✗ Safety not installed. Run: pip install safety${NC}"
fi
echo ""

# 3. SAST - Bandit
echo -e "${YELLOW}[3/7] Running Bandit SAST Scan...${NC}"
if command -v bandit &> /dev/null; then
    bandit -r app/ -f json -o reports/bandit-report.json || true
    bandit -r app/ || true
    echo -e "${GREEN}✓ Bandit scan completed${NC}"
else
    echo -e "${RED}✗ Bandit not installed. Run: pip install bandit${NC}"
fi
echo ""

# 4. SAST - Semgrep
echo -e "${YELLOW}[4/7] Running Semgrep SAST Scan...${NC}"
if command -v semgrep &> /dev/null; then
    semgrep --config=auto --json --output=reports/semgrep-report.json app/ || true
    echo -e "${GREEN}✓ Semgrep scan completed${NC}"
else
    echo -e "${RED}✗ Semgrep not installed. Run: pip install semgrep${NC}"
fi
echo ""

# 5. Container Scanning
echo -e "${YELLOW}[5/7] Running Container Security Scan...${NC}"
if command -v docker &> /dev/null; then
    echo "Building Docker image..."
    docker build -t devsecops-flask:latest -f docker/Dockerfile .
    
    if command -v trivy &> /dev/null; then
        trivy image --severity HIGH,CRITICAL --format json --output reports/trivy-report.json devsecops-flask:latest || true
        trivy image devsecops-flask:latest || true
        echo -e "${GREEN}✓ Trivy scan completed${NC}"
    else
        echo -e "${RED}✗ Trivy not installed. Install: https://github.com/aquasecurity/trivy${NC}"
    fi
else
    echo -e "${RED}✗ Docker not available${NC}"
fi
echo ""

# 6. Code Quality
echo -e "${YELLOW}[6/7] Running Code Quality Checks...${NC}"
if command -v pylint &> /dev/null; then
    pylint app/ --output-format=json > reports/pylint-report.json || true
    echo -e "${GREEN}✓ Pylint completed${NC}"
else
    echo -e "${RED}✗ Pylint not installed. Run: pip install pylint${NC}"
fi
echo ""

# 7. Unit Tests with Coverage
echo -e "${YELLOW}[7/7] Running Unit Tests with Coverage...${NC}"
if command -v pytest &> /dev/null; then
    pytest tests/ --cov=app --cov-report=html --cov-report=json --cov-report=term || true
    echo -e "${GREEN}✓ Tests completed${NC}"
else
    echo -e "${RED}✗ Pytest not installed. Run: pip install pytest pytest-cov${NC}"
fi
echo ""

# Summary
echo "=========================================="
echo -e "${GREEN}Security Scan Pipeline Completed!${NC}"
echo "=========================================="
echo ""
echo "Reports generated in ./reports/ directory:"
echo "  - gitleaks-report.json"
echo "  - safety-report.json"
echo "  - bandit-report.json"
echo "  - semgrep-report.json"
echo "  - trivy-report.json"
echo "  - pylint-report.json"
echo "  - Test coverage: htmlcov/index.html"
echo ""
echo "Review the reports before committing your code!"
