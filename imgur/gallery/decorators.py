import jwt
from django.http import JsonResponse
from django.conf import settings
from functools import wraps
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User


def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get("access_token")
        if not token:
            return JsonResponse({"error": "Token not found"}, status=401)

        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            request.user = User.objects.get(id=user_id)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view
