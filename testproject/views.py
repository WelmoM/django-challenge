import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from .controller import user_account_creation

def health(request):
    return HttpResponse(status=200)


def home(request):
    return HttpResponse("<html><body>Hello World</body></html>")


def create_account(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    data = request.POST or (json.loads(request.body or b"{}") if request.body else {})
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    account_created = user_account_creation(username, email, password)
    if not account_created:
        return JsonResponse({"error": "failed to create account"}, status=400)
    return HttpResponse(status=200)


def login(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    data = request.POST or (json.loads(request.body or b"{}") if request.body else {})
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    if not username or not password:
        return JsonResponse({"error": "username, password required"}, status=400)

    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({"error": "invalid credentials"}, status=400)

    return JsonResponse({"id": user.id, "username": user.username, "email": user.email}, status=200)
