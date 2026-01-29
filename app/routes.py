"""
Application Routes with Security Features
"""
from flask import Blueprint, request, jsonify, render_template_string
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, limiter
from app.models import User
from app.utils import validate_email, validate_password, sanitize_input
import logging

logger = logging.getLogger(__name__)

# Blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
api_bp = Blueprint('api', __name__)

# Home route
@main_bp.route('/')
def index():
    """Home page"""
    return jsonify({
        'message': 'DevSecOps Flask Application',
        'version': '1.0.0',
        'status': 'running'
    })

@main_bp.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        }), 200
    except Exception as e:
        logger.error(f'Health check failed: {str(e)}')
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected'
        }), 503

# Authentication routes
@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    """User registration with input validation"""
    try:
        data = request.get_json()
        
        # Input validation
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password required'}), 400
        
        email = sanitize_input(data['email'])
        password = data['password']
        
        # Validate email format
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password strength
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'User already exists'}), 400
        
        # Create new user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            email=email,
            password=hashed_password,
            username=data.get('username', email.split('@')[0])
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        logger.info(f'New user registered: {email}')
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': new_user.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'Registration error: {str(e)}')
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """User login with JWT token generation"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password required'}), 400
        
        email = sanitize_input(data['email'])
        password = data['password']
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            logger.warning(f'Failed login attempt for: {email}')
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate JWT token
        access_token = create_access_token(identity=user.id)
        
        logger.info(f'User logged in: {email}')
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        }), 200
        
    except Exception as e:
        logger.error(f'Login error: {str(e)}')
        return jsonify({'error': 'Login failed'}), 500

# Protected API routes
@api_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile - Protected route"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'created_at': user.created_at.isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f'Profile fetch error: {str(e)}')
        return jsonify({'error': 'Failed to fetch profile'}), 500

@api_bp.route('/profile', methods=['PUT'])
@jwt_required()
@limiter.limit("10 per hour")
def update_profile():
    """Update user profile - Protected route"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update username if provided
        if 'username' in data:
            username = sanitize_input(data['username'])
            if len(username) < 3:
                return jsonify({'error': 'Username must be at least 3 characters'}), 400
            user.username = username
        
        db.session.commit()
        
        logger.info(f'Profile updated for user: {user.email}')
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'Profile update error: {str(e)}')
        return jsonify({'error': 'Failed to update profile'}), 500

@api_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    """List all users - Protected route"""
    try:
        users = User.query.all()
        
        return jsonify({
            'count': len(users),
            'users': [{
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'created_at': user.created_at.isoformat()
            } for user in users]
        }), 200
        
    except Exception as e:
        logger.error(f'List users error: {str(e)}')
        return jsonify({'error': 'Failed to fetch users'}), 500
