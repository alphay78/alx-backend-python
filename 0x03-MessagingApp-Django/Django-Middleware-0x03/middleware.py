# chats/middleware.py
import logging
from datetime import datetime

# Configure logging to a file
logging.basicConfig(
    filename='requests.log',  # file where logs will be stored
    level=logging.INFO,
    format='%(message)s'
)

class RequestLoggingMiddleware:
    """
    Middleware that logs each user request with timestamp, user, and path.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get user info; use 'AnonymousUser' if not logged in
        user = getattr(request, 'user', None)
        if user is None or not user.is_authenticated:
            user = "AnonymousUser"
        else:
            user = user.username

        # Log the request
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        # Continue processing the request
        response = self.get_response(request)
        return response
