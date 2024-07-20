from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import (
    Image,
    # Post,
    # Vote
)
from .forms import ImageUploadForm


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

    # # Prepare votes data
    # for image in images:
    #     image.upvote_count = Vote.objects.filter(
    #         post=image.post, vote_type="upvote"
    #     ).count()
    #     image.downvote_count = Vote.objects.filter(
    #         post=image.post, vote_type="downvote"
    #     ).count()

    return render(request, "home.html", {"images": images, "form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


# @login_required
# def upvote_post(request, postId):
#     post = get_object_or_404(Post, id=postId)
#     existing_vote = Vote.objects.filter(user=request.user, post=post).first()

#     if existing_vote:
#         if existing_vote.vote_type == "upvote":
#             messages.info(request, "You've already upvoted this post.")
#             return redirect("post_detail", postId=postId)
#         elif existing_vote.vote_type == "downvote":
#             existing_vote.delete()  # Remove the downvote
#             Vote.objects.create(user=request.user, post=post, vote_type="upvote")
#             messages.success(request, "You have upvoted this post.")
#             return redirect("post_detail", postId=postId)
#     else:
#         Vote.objects.create(user=request.user, post=post, vote_type="upvote")
#         messages.success(request, "You have upvoted this post.")
#         return redirect("post_detail", postId=postId)


# @login_required
# def downvote_post(request, postId):
#     post = get_object_or_404(Post, id=postId)
#     existing_vote = Vote.objects.filter(user=request.user, post=post).first()

#     if existing_vote:
#         if existing_vote.vote_type == "downvote":
#             messages.info(request, "You've already downvoted this post.")
#             return redirect("post_detail", postId=postId)
#         elif existing_vote.vote_type == "upvote":
#             existing_vote.delete()  # Remove the upvote
#             Vote.objects.create(user=request.user, post=post, vote_type="downvote")
#             messages.success(request, "You have downvoted this post.")
#             return redirect("post_detail", postId=postId)
#     else:
#         Vote.objects.create(user=request.user, post=post, vote_type="downvote")
#         messages.success(request, "You have downvoted this post.")
#         return redirect("post_detail", postId=postId)
