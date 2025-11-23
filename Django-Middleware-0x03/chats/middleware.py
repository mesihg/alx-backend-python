import logging
from datetime import datetime
import os
from django.conf import settings


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
