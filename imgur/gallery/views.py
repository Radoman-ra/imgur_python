from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .decorators import jwt_required
from .forms import ImageUploadForm
from .forms import UserRegistrationForm
from .models import Image, Vote
import os
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required


class profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_images = Image.objects.filter(user=request.user).order_by("-uploaded_at")
        return render(request, "profile.html", {"user_images": user_images})


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


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                tokens = get_tokens_for_user(user)
                request.session["access_token"] = tokens["access"]
                request.session["refresh_token"] = tokens["refresh"]
                print("Access Token:", tokens["access"])
                print("Refresh Token:", tokens["refresh"])
                return JsonResponse(
                    {
                        "success": True,
                        "access": tokens["access"],
                        "refresh": tokens["refresh"],
                    }
                )
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    form = AuthenticationForm()
    return render(request, "auth/login.html", {"form": form})


def home(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            return redirect("home")
    else:
        form = ImageUploadForm()

    images = Image.objects.all().order_by("-uploaded_at")
    return render(request, "home.html", {"images": images, "form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
@require_POST
def upvote_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if image.user == request.user:
        return JsonResponse({"error": "You cannot upvote your own image"}, status=400)

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
    return JsonResponse(
        {
            "upvotes": image.upvotes,
            "downvotes": image.downvotes,
            "user_vote_status": user_vote_status,
        }
    )


@login_required
@require_POST
def downvote_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if image.user == request.user:
        return JsonResponse({"error": "You cannot downvote your own image"}, status=400)

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
    return JsonResponse(
        {
            "upvotes": image.upvotes,
            "downvotes": image.downvotes,
            "user_vote_status": user_vote_status,
        }
    )


@login_required
@require_POST
@csrf_exempt
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if request.user == image.user:
        if image.image:
            image_path = image.image.path
            if os.path.isfile(image_path):
                os.remove(image_path)
        image.delete()
        return JsonResponse({"success": True})

    return JsonResponse(
        {"error": "You do not have permission to delete this image."}, status=403
    )


def image_detail(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    return render(request, "image_detail.html", {"image": image})


def image_detail_home(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    return render(request, "image_detail_home.html", {"image": image})


@login_required
@require_POST
@csrf_exempt
def update_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if request.user == image.user:
        title = request.POST.get("title")
        description = request.POST.get("description")
        if title:
            image.title = title
        if description:
            image.description = description
        image.save()
        return JsonResponse(
            {"success": True, "title": image.title, "description": image.description}
        )
    return JsonResponse(
        {"error": "You do not have permission to update this image."}, status=403
    )
