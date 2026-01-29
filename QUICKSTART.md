# Quick Start Guide

Get the DevSecOps Flask application running in 5 minutes!

## Prerequisites

- Python 3.9+
- Git
- Docker (optional, for containerized deployment)

## 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/devsecops-flask-app.git
cd devsecops-flask-app

# Run the setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

The setup script will:
- Create virtual environment
- Install dependencies
- Initialize database
- Run tests
- Generate `.env` file with secure keys

## 2. Start the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python run.py
```

The app will be available at: http://localhost:5000

## 3. Test the API

### Health Check
```bash
curl http://localhost:5000/health
```

### Register a User
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecureP@ss123",
    "username": "testuser"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecureP@ss123"
  }'
```

Save the `access_token` from the response.

### Access Protected Endpoint
```bash
curl -X GET http://localhost:5000/api/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 4. Run Security Scans

```bash
# Run all security scans locally
./scripts/run-security-scan.sh
```

This will run:
- GitLeaks (secret detection)
- Safety (dependency scanning)
- Bandit (SAST)
- Semgrep (SAST)
- Trivy (container scanning)
- Pytest (unit tests with coverage)

## 5. Run with Docker

```bash
# Build and run with Docker Compose
cd docker
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app

# Stop
docker-compose down
```

## 6. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

## 7. Deploy to GitHub

### Setup GitHub Repository

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: DevSecOps Flask application"

# Add remote
git remote add origin https://github.com/yourusername/devsecops-flask-app.git

# Push to GitHub
git push -u origin main
```

### Configure GitHub Secrets

Go to Settings → Secrets and variables → Actions and add:

- `SNYK_TOKEN`: Your Snyk API token
- `SONAR_TOKEN`: Your SonarCloud token

### Workflows Will Run Automatically

The following workflows will run on push/PR:
- Security scan pipeline
- SAST analysis
- DAST testing
- CI/CD deployment

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Install new package
pip install package-name
pip freeze > requirements.txt

# Run specific test
pytest tests/test_routes.py::TestAuthRoutes::test_user_login_success -v

# Check code quality
pylint app/

# Format code
black app/

# Run security scan
bandit -r app/

# Build Docker image
docker build -t devsecops-flask:latest -f docker/Dockerfile .

# Run container
docker run -p 5000:5000 devsecops-flask:latest
```

## Troubleshooting

### Port already in use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

### Database errors
```bash
# Reset database
rm app.db
python run.py  # Will recreate tables
```

### Permission denied on scripts
```bash
chmod +x scripts/*.sh
```

## Next Steps

1. Read [README.md](README.md) for detailed documentation
2. Review [SECURITY.md](SECURITY.md) for security policies
3. Check `.github/workflows/` for CI/CD configuration
4. Explore the codebase and customize for your needs
5. Set up monitoring and logging
6. Configure production deployment

## Resources

- **Documentation**: `/docs` directory
- **API Docs**: http://localhost:5000/docs (when implemented)
- **Security Reports**: `/reports` directory
- **Test Coverage**: `/htmlcov/index.html`

## Support

- **Issues**: https://github.com/yourusername/devsecops-flask-app/issues
- **Email**: mucheru@outlook.com
- **LinkedIn**: [James Mucheru](https://linkedin.com/in/jamesmucheru)

---

Happy coding! 🚀🔒
