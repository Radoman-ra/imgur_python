from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Image, Vote
from .forms import ImageUploadForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


class HelloWorld(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"}, status=status.HTTP_200_OK)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация успешна. Теперь вы можете войти.")
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
                messages.error(request, "Неправильный email или пароль.")
        else:
            messages.error(request, "Неправильный email или пароль.")
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
def upvote_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    vote, created = Vote.objects.get_or_create(
        user=request.user, image=image, defaults={"vote": Vote.UPVOTE}
    )

    if not created:
        if vote.vote != Vote.UPVOTE:
            image.downvotes -= 1
            image.upvotes += 1
            vote.vote = Vote.UPVOTE
            vote.save()
        else:
            return JsonResponse(
                {"error": "You have already upvoted this image"}, status=400
            )
    else:
        image.upvotes += 1

    image.save()
    return JsonResponse({"upvotes": image.upvotes, "downvotes": image.downvotes})


@login_required
def downvote_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    vote, created = Vote.objects.get_or_create(
        user=request.user, image=image, defaults={"vote": Vote.DOWNVOTE}
    )

    if not created:
        if vote.vote != Vote.DOWNVOTE:
            image.upvotes -= 1
            image.downvotes += 1
            vote.vote = Vote.DOWNVOTE
            vote.save()
        else:
            return JsonResponse(
                {"error": "You have already downvoted this image"}, status=400
            )
    else:
        image.downvotes += 1

    image.save()
    return JsonResponse({"upvotes": image.upvotes, "downvotes": image.downvotes})


@login_required
@require_POST
@csrf_exempt
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if request.user == image.user:
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
