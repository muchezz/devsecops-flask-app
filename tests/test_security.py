"""
Security Tests
"""
import pytest
import json
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

class TestSecurityHeaders:
    """Test security headers"""
    
    def test_security_headers_present(self, client):
        """Test that security headers are present"""
        response = client.get('/')
        
        # Check for security headers
        assert 'X-Content-Type-Options' in response.headers
        assert 'X-Frame-Options' in response.headers
        assert 'Content-Security-Policy' in response.headers
        assert 'Strict-Transport-Security' in response.headers

class TestAuthentication:
    """Test authentication security"""
    
    def test_register_with_weak_password(self, client):
        """Test that weak passwords are rejected"""
        response = client.post('/auth/register', 
            json={
                'email': 'test@example.com',
                'password': 'weak',
                'username': 'testuser'
            }
        )
        assert response.status_code == 400
        assert b'Password must be at least 8 characters' in response.data
    
    def test_register_with_invalid_email(self, client):
        """Test that invalid emails are rejected"""
        response = client.post('/auth/register',
            json={
                'email': 'invalid-email',
                'password': 'StrongP@ss123',
                'username': 'testuser'
            }
        )
        assert response.status_code == 400
    
    def test_sql_injection_attempt(self, client):
        """Test SQL injection protection"""
        response = client.post('/auth/login',
            json={
                'email': "admin'--",
                'password': "' OR '1'='1"
            }
        )
        assert response.status_code != 200

    def test_rate_limiting(self, client):
        """Test rate limiting on login endpoint"""
        # Attempt multiple logins
        for _ in range(15):
            client.post('/auth/login',
                json={
                    'email': 'test@example.com',
                    'password': 'password'
                }
            )
        
        # Next request should be rate limited
        response = client.post('/auth/login',
            json={
                'email': 'test@example.com',
                'password': 'password'
            }
        )
        assert response.status_code == 429

class TestXSS:
    """Test XSS protection"""
    
    def test_xss_in_username(self, client):
        """Test XSS script injection in username"""
        response = client.post('/auth/register',
            json={
                'email': 'xss@example.com',
                'password': 'StrongP@ss123',
                'username': '<script>alert("XSS")</script>'
            }
        )
        
        # Should either reject or sanitize
        if response.status_code == 201:
            data = json.loads(response.data)
            assert '<script>' not in str(data)

class TestCSRF:
    """Test CSRF protection"""
    
    def test_csrf_token_required(self, client):
        """Test CSRF protection on state-changing operations"""
        # This would need CSRF token implementation
        # Currently a placeholder for demonstration
        pass

class TestAuthorization:
    """Test authorization and access control"""
    
    def test_protected_endpoint_without_token(self, client):
        """Test that protected endpoints require authentication"""
        response = client.get('/api/profile')
        assert response.status_code == 401
    
    def test_invalid_jwt_token(self, client):
        """Test invalid JWT token rejection"""
        headers = {'Authorization': 'Bearer invalid-token'}
        response = client.get('/api/profile', headers=headers)
        assert response.status_code == 422

class TestInputValidation:
    """Test input validation"""
    
    def test_empty_request_body(self, client):
        """Test handling of empty request body"""
        response = client.post('/auth/register', json={})
        assert response.status_code == 400
    
    def test_missing_required_fields(self, client):
        """Test missing required fields"""
        response = client.post('/auth/register',
            json={'email': 'test@example.com'}
        )
        assert response.status_code == 400
    
    def test_malformed_json(self, client):
        """Test malformed JSON handling"""
        response = client.post('/auth/register',
            data='invalid json',
            content_type='application/json'
        )
        assert response.status_code in [400, 415]

class TestErrorHandling:
    """Test secure error handling"""
    
    def test_404_no_stack_trace(self, client):
        """Test 404 doesn't expose stack trace"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        # Should not contain sensitive information
        assert b'Traceback' not in response.data
        assert b'File' not in response.data

class TestSessionManagement:
    """Test session security"""
    
    def test_secure_cookie_flags(self, client):
        """Test that cookies have secure flags"""
        response = client.post('/auth/login',
            json={
                'email': 'test@example.com',
                'password': 'StrongP@ss123'
            }
        )
        
        # Check cookie flags (if using cookies)
        for cookie in response.headers.getlist('Set-Cookie'):
            if 'session' in cookie.lower():
                assert 'HttpOnly' in cookie or 'httponly' in cookie
                assert 'Secure' in cookie or 'secure' in cookie
