from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from gallery.views import (
    HelloWorld,
    register,
    login_view,
    home,
    logout_view,
    # upvote_post,
    # downvote_post,
)
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="IMGUR API",
        default_version="v69",
        description="API documentation for your project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="rmaksim886@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("hello/", HelloWorld.as_view(), name="hello-world"),
    path("accounts/register/", register, name="register"),
    path("accounts/login/", login_view, name="login"),
    path("accounts/logout/", logout_view, name="logout"),
    path("", home, name="home"),
    # path("post/<int:postId>/upvote/", upvote_post, name="upvote_post"),
    # path("post/<int:postId>/downvote/", downvote_post, name="downvote_post"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
