from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

SENSITIVE_PATHS = ["/admin", "/login"]

@shared_task
def detect_anomalies():
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # Check for high request volume (more than 100 in last hour)
    high_volume_ips = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values("ip_address")
        .annotate(count=models.Count("id"))
        .filter(count__gt=100)
    )

    for entry in high_volume_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=entry["ip_address"],
            reason="High volume (>100 req/hour)"
        )

    # Check for access to sensitive paths
    sensitive_logs = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=SENSITIVE_PATHS
    )

    for log in sensitive_logs:
        SuspiciousIP.objects.get_or_create(
            ip_address=log.ip_address,
            reason=f"Accessed sensitive path: {log.path}"
        )

    return "Anomaly detection completed"