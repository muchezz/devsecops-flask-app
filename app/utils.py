"""
Utility Functions for Security and Validation
"""
import re
import html
from typing import Tuple

def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validate password strength
    
    Requirements:
    - At least 8 characters
    - Contains uppercase letter
    - Contains lowercase letter
    - Contains digit
    - Contains special character
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"

def sanitize_input(input_string: str) -> str:
    """
    Sanitize user input to prevent XSS attacks
    
    Args:
        input_string: User input to sanitize
        
    Returns:
        str: Sanitized string
    """
    if not input_string:
        return ""
    
    # HTML escape to prevent XSS
    sanitized = html.escape(str(input_string).strip())
    
    # Remove any potential SQL injection characters
    # This is additional protection; parameterized queries are primary defense
    dangerous_chars = [';', '--', '/*', '*/', 'xp_', 'sp_']
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized

def is_safe_url(url: str) -> bool:
    """
    Check if URL is safe (no open redirect vulnerabilities)
    
    Args:
        url: URL to check
        
    Returns:
        bool: True if safe, False otherwise
    """
    if not url:
        return False
    
    # Only allow relative URLs or URLs from same domain
    if url.startswith('/'):
        return True
    
    # Block external URLs
    dangerous_schemes = ['javascript:', 'data:', 'vbscript:']
    for scheme in dangerous_schemes:
        if url.lower().startswith(scheme):
            return False
    
    return False

def generate_csrf_token() -> str:
    """
    Generate CSRF token
    
    Returns:
        str: CSRF token
    """
    import secrets
    return secrets.token_hex(32)

def validate_csrf_token(token: str, session_token: str) -> bool:
    """
    Validate CSRF token
    
    Args:
        token: Token from request
        session_token: Token from session
        
    Returns:
        bool: True if valid, False otherwise
    """
    import hmac
    return hmac.compare_digest(token, session_token)
