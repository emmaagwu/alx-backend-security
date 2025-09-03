import datetime
from .models import RequestLog
from django.utils.timezone import now


class IPLoggingMiddleware:
    """
    Middleware to log client IP, timestamp, and request path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client IP
        ip = self.get_client_ip(request)
        path = request.path

        # Save log entry
        RequestLog.objects.create(
            ip_address=ip,
            timestamp=now(),
            path=path
        )

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """
        Retrieve client IP address, accounting for proxies.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]  # First in list is client
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
