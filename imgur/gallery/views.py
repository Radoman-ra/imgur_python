from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import ImageUploadForm
from .forms import UserRegistrationForm
from .models import Image, Vote
import os


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


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
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
    print(created)
    if created:
        image.upvotes += 1
        vote.vote = Vote.UPVOTE
        vote.save()
    else:
        if vote.vote == Vote.UPVOTE:
            image.upvotes -= 1
            vote.delete()
        else:
            if vote.vote == Vote.DOWNVOTE:
                image.downvotes -= 1
            image.upvotes += 1
            vote.vote = Vote.UPVOTE
            vote.save()

    image.save()
    return JsonResponse({"upvotes": image.upvotes, "downvotes": image.downvotes})


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
    else:
        if vote.vote == Vote.DOWNVOTE:
            image.downvotes -= 1
            vote.delete()
        else:
            if vote.vote == Vote.UPVOTE:
                image.upvotes -= 1
            image.downvotes += 1
            vote.vote = Vote.DOWNVOTE
            vote.save()

    image.save()
    return JsonResponse({"upvotes": image.upvotes, "downvotes": image.downvotes})


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


@login_required
def profile(request):
    user_images = Image.objects.filter(user=request.user).order_by("-uploaded_at")
    return render(request, "profile.html", {"user_images": user_images})
