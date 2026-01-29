# DevSecOps Flask Application with Comprehensive Security Pipeline

A production-ready Flask application demonstrating DevSecOps best practices with automated security scanning, container security, and CI/CD pipeline integration.

## 🎯 Project Overview

This project showcases:
- **SAST (Static Application Security Testing)** with Bandit, Semgrep, and SonarCloud
- **DAST (Dynamic Application Security Testing)** with OWASP ZAP
- **Dependency Scanning** with Safety and Snyk
- **Container Security Scanning** with Trivy and Grype
- **Secret Detection** with GitLeaks and TruffleHog
- **Infrastructure as Code Security** with Checkov
- **GitHub Actions CI/CD Pipeline**
- **Security Reporting and Compliance**

## 🏗️ Architecture

```
├── app/                    # Flask application
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── utils.py
├── tests/                  # Unit and integration tests
│   ├── test_routes.py
│   └── test_security.py
├── docker/                 # Docker configurations
│   ├── Dockerfile
│   └── docker-compose.yml
├── terraform/              # Infrastructure as Code
│   ├── main.tf
│   └── variables.tf
├── .github/
│   └── workflows/
│       ├── security-scan.yml
│       ├── sast.yml
│       ├── dast.yml
│       └── deploy.yml
├── security/               # Security configurations
│   ├── bandit.yml
│   ├── semgrep-rules.yml
│   └── zap-config.yaml
└── requirements.txt
```

## 🔒 Security Features

### 1. **SAST Tools**
- **Bandit**: Python code security scanner
- **Semgrep**: Multi-language static analysis
- **SonarCloud**: Code quality and security
- **CodeQL**: GitHub's semantic code analysis

### 2. **DAST Tools**
- **OWASP ZAP**: Dynamic application security testing
- **Nikto**: Web server scanner

### 3. **Dependency Scanning**
- **Safety**: Python dependency vulnerability checker
- **Snyk**: Open source vulnerability scanner
- **Dependabot**: Automated dependency updates

### 4. **Container Security**
- **Trivy**: Comprehensive container scanner
- **Grype**: Vulnerability scanner for containers
- **Docker Scout**: Docker's native security scanner

### 5. **Secret Detection**
- **GitLeaks**: Secret detection in code
- **TruffleHog**: High-entropy string detection

### 6. **Infrastructure Security**
- **Checkov**: Terraform/CloudFormation scanner
- **tfsec**: Terraform security scanner

## 🚀 Quick Start

### Prerequisites
```bash
- Python 3.9+
- Docker and Docker Compose
- Git
- GitHub account
```

### Local Development
```bash
# Clone the repository
git clone https://github.com/yourusername/devsecops-flask-app.git
cd devsecops-flask-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run the application
python run.py

# Run tests
pytest tests/ -v

# Run security scans locally
./scripts/run-security-scan.sh
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Access the application
curl http://localhost:5000/health
```

## 🔐 Security Pipeline

### GitHub Actions Workflow

The project includes multiple GitHub Actions workflows:

#### 1. **security-scan.yml** - Comprehensive Security Scan
Runs on every push and pull request:
- Secret scanning with GitLeaks
- Python dependency check with Safety
- SAST with Bandit and Semgrep
- Container scanning with Trivy
- IaC scanning with Checkov

#### 2. **sast.yml** - Static Analysis
- CodeQL analysis
- SonarCloud integration
- Custom security rules

#### 3. **dast.yml** - Dynamic Analysis
- OWASP ZAP baseline scan
- Full spider scan
- API security testing

#### 4. **deploy.yml** - Secure Deployment
- Build Docker image
- Security scan before deployment
- Push to registry
- Deploy to staging/production

## 📊 Security Reports

All security findings are:
- Uploaded as GitHub Actions artifacts
- Integrated with GitHub Security tab
- Sent to security dashboard
- Generate compliance reports

## 🛡️ Security Best Practices Implemented

1. **Least Privilege Access**: Application runs as non-root user
2. **Input Validation**: All user inputs are validated and sanitized
3. **SQL Injection Prevention**: Using parameterized queries
4. **XSS Protection**: Content Security Policy headers
5. **CSRF Protection**: Token-based protection
6. **Authentication**: JWT-based authentication
7. **Rate Limiting**: API rate limiting enabled
8. **Logging**: Security event logging
9. **Encryption**: Data encryption at rest and in transit
10. **Secret Management**: Using environment variables and secrets manager

## 📈 Metrics and Monitoring

- Security scan results tracked over time
- Vulnerability trends
- MTTR (Mean Time To Remediation)
- Code coverage reports
- Performance benchmarks

## 🔧 Configuration

### Environment Variables
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
JWT_SECRET_KEY=your-jwt-secret
ALLOWED_HOSTS=yourdomain.com
```

### Security Thresholds
```yaml
# .github/workflows/security-scan.yml
fail_on_severity: high
max_vulnerabilities: 0
code_coverage_min: 80%
```

## 🐛 Vulnerability Remediation

When vulnerabilities are found:
1. Issue is automatically created in GitHub
2. Security team is notified
3. Fix is prioritized based on severity
4. Retest after remediation
5. Update security baseline

## 📚 Documentation

- [Security Policy](SECURITY.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [API Documentation](docs/API.md)
- [Security Scan Results](docs/SECURITY_RESULTS.md)

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**James Mucheru**
- DevSecOps Engineer
- Email: mucheru@outlook.com
- GitHub: [@muchezz](https://github.com/muchezz)
- LinkedIn: [James Mucheru](https://linkedin.com/in/jamesmucheru)

## 🙏 Acknowledgments

- OWASP for security best practices
- GitHub Security Lab
- Open source security tools community

## 🔗 Related Projects

- [Kubernetes Security Pipeline](https://github.com/yourusername/k8s-security)
- [AWS Infrastructure Security](https://github.com/yourusername/aws-security)
- [CI/CD Security Templates](https://github.com/yourusername/cicd-security)

---

**Note**: This is a demonstration project for DevSecOps practices. Always follow your organization's security policies and compliance requirements.
