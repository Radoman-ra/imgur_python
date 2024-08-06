from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

from .views import refresh_jwt_tokens


class JWTCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get("access_token")
        if access_token:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"


class UnauthorizedRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 401:
            return redirect("login")

        return response


class RefreshTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            tokens = refresh_jwt_tokens(request.user)
            response.set_cookie("access_token", tokens["access"], httponly=True)
            response.set_cookie("refresh_token", tokens["refresh"], httponly=True)
        return response
