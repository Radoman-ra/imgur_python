from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageUploadForm
from .forms import UserRegistrationForm
from .models import Image, Vote
import os
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


def refresh_jwt_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_images = Image.objects.filter(user=request.user).order_by("-uploaded_at")
        form = ImageUploadForm()
        return render(
            request, "profile.html", {"user_images": user_images, "form": form}
        )

    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            return redirect("profile")
        else:
            user_images = Image.objects.filter(user=request.user).order_by(
                "-uploaded_at"
            )
            return render(
                request, "profile.html", {"user_images": user_images, "form": form}
            )


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "auth/register.html", {"form": form})


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                tokens = refresh_jwt_tokens(user)
                response = JsonResponse(
                    {
                        "success": True,
                        "access": tokens["access"],
                        "refresh": tokens["refresh"],
                    }
                )
                response.set_cookie("access_token", tokens["access"], httponly=True)
                response.set_cookie("refresh_token", tokens["refresh"], httponly=True)
                return response
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    csrf_token = get_token(request)
    return render(request, "auth/login.html", {"form": form, "csrf_token": csrf_token})


def home(request):
    images = Image.objects.all().order_by("-uploaded_at")
    return render(request, "home.html", {"images": images})


def logout_view(request):
    logout(request)
    return redirect("home")


class UpvoteImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, image_id):
        image = get_object_or_404(Image, id=image_id)
        if image.user == request.user:
            return Response(
                {"error": "You cannot upvote your own image"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        vote, created = Vote.objects.get_or_create(user=request.user, image=image)
        if created:
            image.upvotes += 1
            vote.vote = Vote.UPVOTE
            vote.save()
            user_vote_status = "upvote"
        else:
            if vote.vote == Vote.UPVOTE:
                image.upvotes -= 1
                vote.delete()
                user_vote_status = "none"
            else:
                if vote.vote == Vote.DOWNVOTE:
                    image.downvotes -= 1
                image.upvotes += 1
                vote.vote = Vote.UPVOTE
                vote.save()
                user_vote_status = "upvote"

        image.save()
        tokens = refresh_jwt_tokens(request.user)
        response = Response(
            {
                "upvotes": image.upvotes,
                "downvotes": image.downvotes,
                "user_vote_status": user_vote_status,
                "access": tokens["access"],
                "refresh": tokens["refresh"],
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie("access_token", tokens["access"], httponly=True)
        response.set_cookie("refresh_token", tokens["refresh"], httponly=True)
        return response


class DownvoteImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, image_id):
        image = get_object_or_404(Image, id=image_id)
        if image.user == request.user:
            return Response(
                {"error": "You cannot downvote your own image"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        vote, created = Vote.objects.get_or_create(user=request.user, image=image)
        if created:
            image.downvotes += 1
            vote.vote = Vote.DOWNVOTE
            vote.save()
            user_vote_status = "downvote"
        else:
            if vote.vote == Vote.DOWNVOTE:
                image.downvotes -= 1
                vote.delete()
                user_vote_status = "none"
            else:
                if vote.vote == Vote.UPVOTE:
                    image.upvotes -= 1
                image.downvotes += 1
                vote.vote = Vote.DOWNVOTE
                vote.save()
                user_vote_status = "downvote"

        image.save()

        tokens = get_tokens_for_user(request.user)

        response = Response(
            {
                "upvotes": image.upvotes,
                "downvotes": image.downvotes,
                "user_vote_status": user_vote_status,
                "access": tokens["access"],
                "refresh": tokens["refresh"],
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie("access_token", tokens["access"], httponly=True)
        response.set_cookie("refresh_token", tokens["refresh"], httponly=True)

        return response


class DeleteImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, image_id):
        image = get_object_or_404(Image, id=image_id)
        if request.user == image.user:
            if image.image:
                image_path = image.image.path
                if os.path.isfile(image_path):
                    os.remove(image_path)
            image.delete()
            return Response({"success": True}, status=status.HTTP_200_OK)

        return Response(
            {"error": "You do not have permission to delete this image."},
            status=status.HTTP_403_FORBIDDEN,
        )


def image_detail(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    return render(request, "image_detail.html", {"image": image})


def image_detail_home(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    return render(request, "image_detail_home.html", {"image": image})


class UpdateImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, image_id):
        image = get_object_or_404(Image, id=image_id)
        if request.user == image.user:
            title = request.POST.get("title")
            description = request.POST.get("description")
            if title:
                image.title = title
            if description:
                image.description = description
            image.save()
            return Response(
                {
                    "success": True,
                    "title": image.title,
                    "description": image.description,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "You do not have permission to update this image."},
            status=status.HTTP_403_FORBIDDEN,
        )
