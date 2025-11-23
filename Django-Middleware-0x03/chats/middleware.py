import logging
from datetime import datetime
import os
from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils import timezone


class RequestLoggingMiddleware:
    """
    Middleware that logs user's requests to a file, including timestamp, user, and request path.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware.

        Args:
            get_response: The next middleware or view in the chain
        """
        self.get_response = get_response

        log_file = os.path.join(settings.BASE_DIR, 'requests.log')

        self.logger = logging.getLogger('request_logger')
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)

            formatter = logging.Formatter('%(message)s')
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

    def __call__(self, request):
        """
        Process the request and log the information.
        """
        if request.user.is_authenticated:
            user = request.user.username
        else:
            user = "Anonymous"

        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        response = self.get_response(request)

        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging app during certain hours.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware.
        """
        self.get_response = get_response

        self.start_hour = 6  # 6 AM
        self.end_hour = 21   # 9 PM (21:00)

    def __call__(self, request):
        """
        Process the request and check if access is allowed during current time.
        """
        current_time = timezone.now()
        current_hour = current_time.hour

        chat_paths = ['/api/v1/', '/admin/', '/conversations', '/messages']

        is_chat_request = any(request.path.startswith(path)
                              for path in chat_paths if path != '/admin/')

        if is_chat_request and not (self.start_hour <= current_hour < self.end_hour):
            forbidden_message = f"""
            <html>
            <head><title>Access Restricted</title></head>
            <body>
                <h1>403 Forbidden</h1>
                <p>Access to the messaging app is restricted.</p>
                <p>Please try again between 6:00 AM and 9:00 PM.</p>
                <p>Current server time: {current_time.strftime('%H:%M:%S')}</p>
            </body>
            </html>
            """
            return HttpResponseForbidden(forbidden_message)

        response = self.get_response(request)

        return response
