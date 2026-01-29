# Project Structure

Complete overview of the DevSecOps Flask Application architecture and organization.

## Directory Structure

```
devsecops-flask-app/
│
├── .github/
│   └── workflows/           # GitHub Actions CI/CD workflows
│       ├── security-scan.yml    # Comprehensive security scanning
│       ├── dast.yml             # Dynamic application security testing
│       └── deploy.yml           # CI/CD deployment pipeline
│
├── app/                     # Application source code
│   ├── __init__.py         # Application factory
│   ├── routes.py           # API endpoints and routes
│   ├── models.py           # Database models
│   └── utils.py            # Utility functions and validators
│
├── tests/                   # Test suite
│   ├── test_routes.py      # Route unit tests
│   └── test_security.py    # Security tests
│
├── docker/                  # Docker configuration
│   ├── Dockerfile          # Production-ready container image
│   └── docker-compose.yml  # Local development orchestration
│
├── security/                # Security configurations
│   ├── bandit.yml          # Bandit SAST configuration
│   └── zap-rules.tsv       # OWASP ZAP scanning rules
│
├── scripts/                 # Automation scripts
│   ├── setup.sh            # Project setup automation
│   └── run-security-scan.sh # Local security scanning
│
├── docs/                    # Additional documentation
│   └── (created as needed)
│
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── run.py                   # Application entry point
├── .gitignore              # Git ignore rules
├── README.md               # Project overview
├── QUICKSTART.md           # Quick start guide
├── SECURITY.md             # Security policy
└── PROJECT_STRUCTURE.md    # This file
```

## Component Details

### Application Layer (`app/`)

#### `__init__.py` - Application Factory
- Creates and configures Flask application
- Initializes extensions (SQLAlchemy, JWT, Limiter, Talisman)
- Sets up security headers
- Configures logging
- Registers blueprints
- Error handlers

#### `routes.py` - API Endpoints
**Main Blueprint**
- `/` - Index/welcome page
- `/health` - Health check endpoint

**Auth Blueprint** (`/auth`)
- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication

**API Blueprint** (`/api`)
- `GET /api/profile` - Get user profile (protected)
- `PUT /api/profile` - Update user profile (protected)
- `GET /api/users` - List all users (protected)

#### `models.py` - Database Models
- `User` - User model with secure password storage
  - Fields: id, email, username, password, created_at, updated_at, is_active
  - Methods: to_dict()

#### `utils.py` - Utility Functions
- `validate_email()` - Email format validation
- `validate_password()` - Password strength validation
- `sanitize_input()` - XSS prevention
- `is_safe_url()` - Open redirect prevention
- `generate_csrf_token()` - CSRF token generation
- `validate_csrf_token()` - CSRF token validation

### Testing Layer (`tests/`)

#### `test_routes.py` - Functional Tests
- Health check tests
- User registration tests
- Authentication tests
- Protected endpoint tests
- Profile management tests

#### `test_security.py` - Security Tests
- Security headers validation
- Authentication security
- SQL injection prevention
- XSS protection
- CSRF protection
- Rate limiting
- Input validation
- Error handling
- Session management

### Infrastructure Layer

#### Docker Configuration
**Dockerfile**
- Multi-stage build for smaller image
- Non-root user execution
- Security best practices
- Health checks
- Gunicorn WSGI server

**docker-compose.yml**
- Application service
- PostgreSQL database
- Redis cache
- Networking configuration
- Volume management
- Health checks

### Security Layer

#### GitHub Actions Workflows

**security-scan.yml** - Comprehensive Security Pipeline
Jobs:
1. `secret-scan` - GitLeaks, TruffleHog
2. `dependency-scan` - Safety, Snyk
3. `sast-scan` - Bandit, Semgrep
4. `codeql-analysis` - GitHub CodeQL
5. `container-scan` - Trivy, Grype
6. `iac-scan` - Checkov, tfsec
7. `sonarcloud` - SonarCloud analysis
8. `security-report` - Consolidated reporting

**dast.yml** - Dynamic Security Testing
Jobs:
1. `dast-scan` - OWASP ZAP baseline and full scans
2. `api-security-test` - API endpoint security testing
3. `nikto-scan` - Web server vulnerability scanning

**deploy.yml** - CI/CD Pipeline
Jobs:
1. `build-and-test` - Build and unit tests
2. `security-sast` - SAST security gate
3. `security-secrets` - Secret scanning gate
4. `build-docker` - Docker image build
5. `security-container` - Container security gate
6. `deploy-staging` - Staging deployment
7. `security-dast` - DAST security gate
8. `deploy-production` - Production deployment
9. `post-deployment-tests` - Smoke tests

### Configuration Files

#### `.gitignore`
- Python artifacts
- Virtual environments
- IDE files
- Testing artifacts
- Security reports
- Database files
- Environment variables
- Logs

#### `requirements.txt`
Production dependencies:
- Flask 3.0.0
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-Limiter
- Flask-Talisman
- PostgreSQL driver
- Gunicorn
- Other core dependencies

#### `requirements-dev.txt`
Development dependencies:
- pytest
- pytest-cov
- pytest-flask
- bandit
- safety
- semgrep
- pylint
- black
- flake8
- mypy

## Security Implementation

### Defense in Depth

**Layer 1: Input Validation**
- Email format validation
- Password strength requirements
- Input sanitization
- Type checking

**Layer 2: Authentication & Authorization**
- JWT-based authentication
- Password hashing (PBKDF2-SHA256)
- Token expiration
- Role-based access control

**Layer 3: Application Security**
- SQL injection prevention (ORM)
- XSS protection (CSP headers)
- CSRF protection
- Rate limiting
- Secure session management

**Layer 4: Transport Security**
- HTTPS enforcement
- TLS/SSL configuration
- Secure cookies (HttpOnly, Secure flags)
- HSTS headers

**Layer 5: Infrastructure Security**
- Container hardening
- Non-root execution
- Minimal base images
- Regular updates
- Secret management

### Security Scanning Integration

**Pre-commit** (Local)
- Run security scan script
- Check for secrets
- Lint code
- Run tests

**CI/CD** (GitHub Actions)
- Automated on every push/PR
- Multiple security tools
- Security gates before deployment
- Continuous monitoring

**Scheduled** (Weekly)
- Comprehensive scans
- Dependency updates check
- Container image scanning
- DAST on production

## Development Workflow

### Local Development
1. Setup environment: `./scripts/setup.sh`
2. Activate venv: `source venv/bin/activate`
3. Run app: `python run.py`
4. Run tests: `pytest tests/ -v`
5. Security scan: `./scripts/run-security-scan.sh`

### Contributing
1. Create feature branch
2. Make changes
3. Run tests locally
4. Run security scans
5. Create pull request
6. CI/CD runs automatically
7. Code review
8. Merge to main

### Deployment
1. Push to main branch
2. CI/CD pipeline triggered
3. Security gates passed
4. Deploy to staging
5. DAST on staging
6. Deploy to production
7. Post-deployment tests

## Monitoring & Logging

### Application Logs
- Request/response logging
- Error logging
- Security event logging
- Performance metrics

### Security Monitoring
- Failed authentication attempts
- Rate limit violations
- Suspicious patterns
- Vulnerability alerts

### Metrics
- Request rate
- Response time
- Error rate
- Security scan results

## Best Practices

### Code Quality
- Follow PEP 8 style guide
- Use type hints
- Write docstrings
- Maintain test coverage >80%
- Regular code reviews

### Security
- Never commit secrets
- Keep dependencies updated
- Run security scans regularly
- Follow OWASP guidelines
- Implement defense in depth

### Testing
- Unit tests for all functions
- Integration tests for APIs
- Security tests for vulnerabilities
- Performance tests for scalability
- End-to-end tests for user flows

## Troubleshooting

### Common Issues

**Import errors**
- Activate virtual environment
- Install requirements

**Database errors**
- Initialize database: `python run.py`
- Check DATABASE_URL

**Port conflicts**
- Change PORT environment variable
- Kill process using port 5000

**Docker issues**
- Rebuild image: `docker-compose build`
- Check logs: `docker-compose logs`

## Maintenance

### Regular Tasks
- Weekly dependency updates
- Monthly security audits
- Quarterly penetration testing
- Annual code review

### Updates
- Monitor security advisories
- Apply patches promptly
- Test before deployment
- Document changes

---

For more information, see:
- [README.md](README.md) - Project overview
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [SECURITY.md](SECURITY.md) - Security policy
