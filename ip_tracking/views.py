from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit

# Example: Anonymous users → 5 req/min, Authenticated → 10 req/min
@ratelimit(key="ip", rate="5/m", block=True)
@ratelimit(key="user_or_ip", rate="10/m", block=True)
def login_view(request):
    if request.method == "POST":
        # Normally, you'd authenticate user here
        return JsonResponse({"message": "Login attempt"}, status=200)
    return JsonResponse({"message": "Send POST request"}, status=405)


# Optional: custom view for exceeded limit
def ratelimit_exceeded_view(request, exception=None):
    return JsonResponse(
        {"error": "Too many requests, slow down!"},
        status=429
    )
