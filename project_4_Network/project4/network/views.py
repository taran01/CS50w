from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

from .models import *


def index(request):
    user = request.user
    posts = Post.objects.all().order_by("-timestamp")
    page_number = request.GET.get("page", 1)

    paginator = Paginator(posts, 10)

    try:
        items_page = paginator.page(page_number)
    except PageNotAnInteger:
        items_page = paginator.page(1)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)

    if user.is_authenticated:
        likes = user.likes.all()
    else:
        likes = []

    return render(
        request,
        "network/index.html",
        {"items_page": items_page, "title": "All Posts", "likes": likes},
    )


@login_required(login_url="/login")
def following(request):
    user = request.user
    following = user.following.all()
    following_users = [user.user for user in following]
    posts = Post.objects.filter(user__in=following_users).order_by("-timestamp")
    likes = user.likes.all()

    page_number = request.GET.get("page", 1)
    paginator = Paginator(posts, 10)

    try:
        items_page = paginator.page(page_number)
    except PageNotAnInteger:
        items_page = paginator.page(1)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)

    return render(
        request,
        "network/index.html",
        {"items_page": items_page, "title": "Following Posts", "likes": likes},
    )


def profile_page(request, username):
    try:
        profile_user = User.objects.get(username=username)
    except:
        return render(request, "network/profile.html", {"error": username})

    posts = Post.objects.filter(user=profile_user).order_by("-timestamp")
    followers = Followers.objects.get(user=profile_user).followers.count()
    following = profile_user.following.count()

    try:
        Followers.objects.get(user=profile_user, followers=request.user)
        follows = True
    except:
        follows = False

    page_number = request.GET.get("page", 1)
    paginator = Paginator(posts, 10)

    try:
        items_page = paginator.page(page_number)
    except PageNotAnInteger:
        items_page = paginator.page(1)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        likes = request.user.likes.all()
    else:
        likes = []

    return render(
        request,
        "network/profile.html",
        {
            "profile_user": profile_user,
            "items_page": items_page,
            "followers": followers,
            "following": following,
            "follows": follows,
            "likes": likes
        },
    )


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url="/login")
def new_post(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        content = request.POST["content"]
        if not content:
            posts = Post.objects.all().order_by("-timestamp")
            return render(
                request,
                "network/index.html",
                {"posts": posts, "form_message": "Post cannot be empty."},
            )

        post = Post.objects.create(user=user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


@csrf_exempt
def edit_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    id = data.get("id")
    content = data.get("content")

    post = Post.objects.get(pk=id)
    if post.user != request.user:
        return JsonResponse({"error": "Not valid user."}, status=400)

    post.content = content
    post.save()

    return JsonResponse({"message": "Edited successfully."}, status=201)


@login_required(login_url="/login")
@csrf_exempt
def change_follow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    profile = User.objects.get(id=data.get("profile_id"))
    value = data.get("value")
    user = request.user

    if value == "unfollow":
        obj = Followers.objects.get(user=profile)
        obj.followers.remove(user)
        obj.save()

        return JsonResponse({"message": "unfollowed"}, status=201)

    elif value == "follow":
        try:
            obj = Followers.objects.create(user=profile)
        except IntegrityError:
            obj = Followers.objects.get(user=profile)

        obj.followers.add(user)
        obj.save()

        return JsonResponse({"message": "followed"}, status=201)


@csrf_exempt
def change_like(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "need to login in"}, status=403)

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    post = Post.objects.get(id=data.get("post_id"))
    value = data.get("value")
    user = request.user

    if value == "like":
        user.likes.remove(post)
        post.likes -= 1
        post.save()
        return JsonResponse({"message": "unliked post"}, status=201)

    elif value == "unlike":
        user.likes.add(post)
        post.likes += 1
        post.save()
        return JsonResponse({"message": "liked post"}, status=201)
