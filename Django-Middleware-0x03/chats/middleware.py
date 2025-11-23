import logging
from datetime import datetime
import os
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse
from django.utils import timezone
from collections import defaultdict, deque
import time


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


class OffensiveLanguageMiddleware:
    """
    Middleware that limits the number of chat messages a user can send within a certain time window,
    based on their IP address. Implements rate limiting for POST requests to prevent spam.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware.
        """
        self.get_response = get_response

        self.max_messages_per_minute = 5
        self.time_window = 60

        self.ip_requests = defaultdict(deque)

        self.last_cleanup = time.time()
        self.cleanup_interval = 300

    def get_client_ip(self, request):
        """
        Get the client's IP address from the request.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip

    def cleanup_old_requests(self):
        """
        Remove old request timestamps that are outside the time window.
        """
        current_time = time.time()
        cutoff_time = current_time - self.time_window

        for ip, timestamps in list(self.ip_requests.items()):
            while timestamps and timestamps[0] < cutoff_time:
                timestamps.popleft()

            if not timestamps:
                del self.ip_requests[ip]

    def is_rate_limited(self, ip_address):
        """
        Check if the IP address has exceeded the rate limit.
        """
        current_time = time.time()
        cutoff_time = current_time - self.time_window

        timestamps = self.ip_requests[ip_address]

        while timestamps and timestamps[0] < cutoff_time:
            timestamps.popleft()

        return len(timestamps) >= self.max_messages_per_minute

    def record_request(self, ip_address):
        """
        Record a new request for the IP address.
        """
        current_time = time.time()
        self.ip_requests[ip_address].append(current_time)

    def __call__(self, request):
        """
        Process the request and check for rate limiting on POST requests to messaging endpoints.
        """
        current_time = time.time()
        if current_time - self.last_cleanup > self.cleanup_interval:
            self.cleanup_old_requests()
            self.last_cleanup = current_time

        messaging_paths = [
            '/api/v1/messages/', '/api/v1/conversations/', '/messages/', '/conversations/']
        is_messaging_post = (
            request.method == 'POST' and
            any(request.path.startswith(path) for path in messaging_paths)
        )

        if is_messaging_post:
            client_ip = self.get_client_ip(request)

            if self.is_rate_limited(client_ip):
                rate_limit_message = f"""
                <html>
                <head><title>Rate Limit Exceeded</title></head>
                <body>
                    <h1>429 Too Many Requests</h1>
                    <p>You have exceeded the rate limit for sending messages.</p>
                    <p>Limit: {self.max_messages_per_minute} messages per minute</p>
                    <p>Please wait before sending another message.</p>
                    <p>Your IP: {client_ip}</p>
                    <p>Time: {datetime.now().strftime('%H:%M:%S')}</p>
                </body>
                </html>
                """
                response = HttpResponse(rate_limit_message, status=429)
                # Suggest retry time
                response['Retry-After'] = str(self.time_window)
                return response

            self.record_request(client_ip)

        response = self.get_response(request)

        return response


class RolepermissionMiddleware:
    """
    Middleware that checks the user's role before allowing access to specific actions.
    Only admin and moderator users are allowed to perform certain privileged operations.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware.
        """
        self.get_response = get_response

        self.allowed_roles = ['admin', 'moderator']

        self.protected_paths = [
            '/admin/',
            '/api/v1/admin/',
            '/api/v1/users/',
            '/api/v1/conversations/delete/',
            '/api/v1/messages/delete/',
            '/api/v1/moderation/',
        ]

        self.protected_methods = ['POST', 'PUT', 'PATCH', 'DELETE']

    def is_protected_path(self, request_path):
        """
        Check if the request path requires privileged access.
        """
        return any(request_path.startswith(path) for path in self.protected_paths)

    def is_protected_operation(self, request):
        """
        Check if the request is a protected operation that requires role check.
        """
        if self.is_protected_path(request.path):
            return True

        if (request.method in self.protected_methods and
                request.path.startswith('/api/v1/')):
            allowed_for_all = [
                '/api/v1/conversations/',
                '/api/v1/messages/',
            ]

            if any(request.path == path or
                   (request.path.startswith(path) and request.method == 'POST')
                   for path in allowed_for_all):
                return False

            return True

        return False

    def has_required_role(self, user):
        """
        Check if the user has the required role for privileged operations.
        """
        if not user.is_authenticated:
            return False

        return hasattr(user, 'role') and user.role in self.allowed_roles

    def __call__(self, request):
        """
        Process the request and check user role for protected operations.
        """
        if self.is_protected_operation(request):
            if not self.has_required_role(request.user):
                if not request.user.is_authenticated:
                    reason = "Authentication required"
                    user_info = "Not authenticated"
                else:
                    reason = "Insufficient privileges"
                    user_role = getattr(request.user, 'role', 'unknown')
                    user_info = f"User role: {user_role}"

                forbidden_message = f"""
                <html>
                <head><title>Access Denied</title></head>
                <body>
                    <h1>403 Forbidden</h1>
                    <p><strong>Access Denied:</strong> {reason}</p>
                    <p>This operation requires admin or moderator privileges.</p>
                    <p><strong>Required roles:</strong> {', '.join(self.allowed_roles)}</p>
                    <p><strong>Your status:</strong> {user_info}</p>
                    <p><strong>Requested path:</strong> {request.path}</p>
                    <p><strong>Method:</strong> {request.method}</p>
                    <p><strong>Time:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
                </body>
                </html>
                """

                return HttpResponseForbidden(forbidden_message)

        response = self.get_response(request)

        return response
