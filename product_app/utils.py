import jwt
from datetime import datetime, timedelta
from functools import wraps
from jwt import ExpiredSignatureError, InvalidTokenError

from django.http import JsonResponse
from django.conf.global_settings import SECRET_KEY

def generate_signed_token_for_user(user):
    """
    Generate a signed JWT token for the given user.
    """
    payload = {
        'user_id': str(user.id),
        'username': user.username,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def token_required(view_func):
    """
    Decorator to validate JWT token before executing the route logic.
    """
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Extract token from the Authorization header
        auth_header = request.headers.get('Authorization', '')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'Message': 'Token missing or invalid format'}, status=401)

        token = auth_header.split(' ')[1]  # Extract the token
        try:
            # Decode the token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            # Attach the decoded payload to the request for use in the view
            request.user_data = payload
        except ExpiredSignatureError:
            return JsonResponse({'Message': 'Token has expired, please login again to get a new token'}, status=401)
        except InvalidTokenError:
            return JsonResponse({'Message': 'Invalid token'}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapped_view
