# IP Tracking & Security (Django Project)

This project is part of the **ALX Backend Security** track.  
It focuses on **IP tracking, geolocation, rate limiting, and anomaly detection** using Django.

---

## 🚀 Features

- **IP Tracking**: Capture and log client IP addresses.
- **Geolocation**: Use [`django-ip-geolocation`](https://pypi.org/project/django-ip-geolocation/) to get location details.
- **Rate Limiting**: Protect sensitive endpoints with [`django-ratelimit`](https://pypi.org/project/django-ratelimit/).
- **Anomaly Detection**: Detect suspicious IPs (e.g., too many requests, accessing sensitive paths).
- **Celery Integration**: Run background tasks to monitor traffic hourly.

---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/alx-backend-security.git
   cd alx-backend-security
