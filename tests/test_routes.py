"""
Unit Tests for Routes
"""
import pytest
import json
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

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

@pytest.fixture
def test_user(app):
    """Create test user"""
    with app.app_context():
        user = User(
            email='test@example.com',
            username='testuser',
            password=generate_password_hash('TestP@ss123')
        )
        db.session.add(user)
        db.session.commit()
        return user

class TestMainRoutes:
    """Test main routes"""
    
    def test_index_route(self, client):
        """Test index route"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'version' in data
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'

class TestAuthRoutes:
    """Test authentication routes"""
    
    def test_user_registration_success(self, client):
        """Test successful user registration"""
        response = client.post('/auth/register',
            json={
                'email': 'newuser@example.com',
                'password': 'NewP@ss123',
                'username': 'newuser'
            }
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'user_id' in data
    
    def test_duplicate_user_registration(self, client, test_user):
        """Test duplicate user registration"""
        response = client.post('/auth/register',
            json={
                'email': 'test@example.com',
                'password': 'TestP@ss123',
                'username': 'testuser'
            }
        )
        assert response.status_code == 400
    
    def test_user_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post('/auth/login',
            json={
                'email': 'test@example.com',
                'password': 'TestP@ss123'
            }
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
    
    def test_user_login_invalid_credentials(self, client, test_user):
        """Test login with invalid credentials"""
        response = client.post('/auth/login',
            json={
                'email': 'test@example.com',
                'password': 'wrongpassword'
            }
        )
        assert response.status_code == 401

class TestAPIRoutes:
    """Test API routes"""
    
    def get_auth_token(self, client):
        """Helper to get authentication token"""
        # Register user
        client.post('/auth/register',
            json={
                'email': 'api@example.com',
                'password': 'ApiP@ss123',
                'username': 'apiuser'
            }
        )
        
        # Login
        response = client.post('/auth/login',
            json={
                'email': 'api@example.com',
                'password': 'ApiP@ss123'
            }
        )
        data = json.loads(response.data)
        return data['access_token']
    
    def test_get_profile_authenticated(self, client):
        """Test getting profile with authentication"""
        token = self.get_auth_token(client)
        headers = {'Authorization': f'Bearer {token}'}
        
        response = client.get('/api/profile', headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'email' in data
    
    def test_get_profile_unauthenticated(self, client):
        """Test getting profile without authentication"""
        response = client.get('/api/profile')
        assert response.status_code == 401
    
    def test_update_profile(self, client):
        """Test updating user profile"""
        token = self.get_auth_token(client)
        headers = {'Authorization': f'Bearer {token}'}
        
        response = client.put('/api/profile',
            json={'username': 'updateduser'},
            headers=headers
        )
        assert response.status_code == 200
    
    def test_list_users(self, client):
        """Test listing users"""
        token = self.get_auth_token(client)
        headers = {'Authorization': f'Bearer {token}'}
        
        response = client.get('/api/users', headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'users' in data
        assert 'count' in data
