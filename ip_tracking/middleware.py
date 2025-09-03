from django.http import HttpResponseForbidden
from django.utils.timezone import now
from django.core.cache import cache
from ipgeolocation import geolocator
from .models import RequestLog, BlockedIP


class IPLoggingMiddleware:
    """
    Middleware to log client IP, geolocation, and block requests if IP is blacklisted.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Block request if IP is blacklisted
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        # Get geolocation (cached for 24h)
        geo_data = cache.get(f"geo_{ip}")
        if not geo_data:
            try:
                geo_data = geolocator(ip)
                cache.set(f"geo_{ip}", geo_data, 60 * 60 * 24)  # 24 hours
            except Exception:
                geo_data = {"country": None, "city": None}

        # Log request
        RequestLog.objects.create(
            ip_address=ip,
            timestamp=now(),
            path=request.path,
            country=geo_data.get("country"),
            city=geo_data.get("city"),
        )

        return self.get_response(request)

    def get_client_ip(self, request):
        """
        Retrieve client IP address, accounting for proxies.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
