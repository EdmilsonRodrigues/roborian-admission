import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_jwt_token(user_email):
    # Create a payload containing the user ID and expiration time
    payload = {
        'user_email': user_email,
        'exp': datetime.now() + timedelta(hours=1)
    }
    # Generate the JWT token
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token


def verify_jwt_token(token):
    try:
        # Decode and verify the JWT token
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        # Token is expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None
    