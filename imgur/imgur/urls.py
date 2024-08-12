from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic.base import RedirectView
from gallery.views import (
    home,
    image_detail,
    ProfileView,
    register,
    login_view,
    logout_view,
    UpvoteImageView,
    DownvoteImageView,
    DeleteImageView,
    UpdateImageView,
    image_detail_home,
)

# API schema view configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Imgur Clone API",
        default_version="v1",
        description="API documentation for the Imgur Clone project",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
    # Admin and main views
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("image/<int:image_id>/", image_detail, name="image-detail"),
    path("home_image/<int:image_id>/", image_detail_home, name="image-detail-home"),
    path(
        "image/<int:image_id>/delete/", DeleteImageView.as_view(), name="delete-image"
    ),
    path(
        "image/<int:image_id>/update/", UpdateImageView.as_view(), name="update-image"
    ),
    path("api/profile/", ProfileView.as_view(), name="profile"),
    # Authentication views
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # Voting views
    path("upvote/<int:image_id>/", UpvoteImageView.as_view(), name="upvote-image"),
    path(
        "downvote/<int:image_id>/", DownvoteImageView.as_view(), name="downvote-image"
    ),
    # API schema views
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
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", RedirectView.as_view(url="/")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
