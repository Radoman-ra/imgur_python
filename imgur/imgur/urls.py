from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from gallery.views import (
    register,
    login_view,
    home,
    logout_view,
    upvote_image,
    downvote_image,
    image_detail,
    delete_image,
    update_image,
    profile,
)

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
                  path("accounts/register/", register, name="register"),
                  path("accounts/login/", login_view, name="login"),
                  path("accounts/logout/", logout_view, name="logout"),
                  path("", home, name="home"),
                  path("upvote/<int:image_id>/", upvote_image, name="upvote-image"),
                  path("downvote/<int:image_id>/", downvote_image, name="downvote-image"),
                  path("image/<int:image_id>/", image_detail, name="image-detail"),
                  path("image/<int:image_id>/delete/", delete_image, name="delete-image"),
                  path("image/<int:image_id>/update/", update_image, name="update-image"),
                  path("profile/", profile, name="profile"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
