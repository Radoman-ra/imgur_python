import jwt
from django.http import JsonResponse
from functools import wraps
from django.conf import settings


def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.session.get("access_token")
        if not token:
            return JsonResponse(
                {"detail": "Authentication credentials were not provided."}, status=401
            )

        try:
            # Пытаемся декодировать токен
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            # Здесь можно добавить дополнительную проверку или обработку декодированного токена
        except jwt.ExpiredSignatureError:
            return JsonResponse({"detail": "Token has expired."}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"detail": "Invalid token."}, status=401)

        # Добавляем декодированный токен в request для использования в view
        request.user = decoded_token  # Или другое поле, которое вам нужно
        return view_func(request, *args, **kwargs)

    return _wrapped_view
