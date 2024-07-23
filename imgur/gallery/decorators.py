from functools import wraps
from django.http import JsonResponse


def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.session.get("access_token")
        if not token:
            return JsonResponse(
                {"detail": "Authentication credentials were not provided."}, status=401
            )
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        return view_func(request, *args, **kwargs)

    return _wrapped_view
