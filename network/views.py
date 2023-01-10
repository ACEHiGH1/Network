import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post, Profile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Function for the index page.


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'page_obj': page_obj}
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html", {
            'page': 1
        })


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile(user=user)
            profile.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# Function that creates a new post based on the form data, and saves it in the database.


def newPost(request):
    if request.method == "POST":
        content = request.POST["newPost"]
    post = Post(user=request.user, content=content)
    post.save()
    return HttpResponseRedirect(reverse("index"))

# Function for the personal profile page.
# Gets all the information from the database and passes it to the page as parameters.


def viewUsername(request, username):
    user = User.objects.get(username=username)
    userProfile = Profile.objects.get(user=user)

    followersCount = userProfile.followers.all().count()
    followingCount = userProfile.following.all().count()

    posts = Post.objects.filter(user=user).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/viewUsername.html", {
        'userProfile': userProfile,
        'page_obj': page_obj,
        'followingCount': followingCount,
        'followersCount': followersCount
    })

# Back-end function that changes the database when a user follows a profile.


def follow(request, username):
    followProfile = Profile.objects.get(
        user=User.objects.get(username=username))
    userProfile = Profile.objects.get(
        user=User.objects.get(username=request.user.username))

    followProfile.followers.add(User.objects.get(id=userProfile.user.id))
    userProfile.following.add(User.objects.get(id=followProfile.user.id))

    followProfile.save()
    userProfile.save()
    return HttpResponseRedirect(reverse("viewUsername", kwargs={'username': username}))

# Back-end function that changes the database when a user unfollows a profile.


def unfollow(request, username):
    followProfile = Profile.objects.get(
        user=User.objects.get(username=username))
    userProfile = Profile.objects.get(
        user=User.objects.get(username=request.user.username))

    followProfile.followers.remove(User.objects.get(id=userProfile.user.id))
    userProfile.following.remove(User.objects.get(id=followProfile.user.id))

    followProfile.save()
    userProfile.save()
    return HttpResponseRedirect(reverse("viewUsername", kwargs={'username': username}))

# Function for the following page that displays only the posts of the people you follow.


def following(request):
    following = Profile.objects.get(
        user=User.objects.get(username=request.user.username)).following.all()
    posts = []
    for f in following:
        author = User.objects.get(id=f.id)
        posts += Post.objects.filter(user=author).order_by("timestamp").all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'page_obj': page_obj}
    )


# API that returns post contents and saves the changes in post content to database.
@csrf_exempt
def editPost(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    if request.method == "POST":
        data = json.loads(request.body)
        # Get contents of post
        postId = data.get("id", "")
        content = data.get("content", "")

        # Saves the new changes of the post to database.
        post = Post.objects.get(id=postId)
        post.content = content
        post.save()
        return JsonResponse({"message": "Post edited successfully."}, status=201)

# API that changes the database once a posted is liked


@csrf_exempt
def likePost(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    if request.method == "POST":
        data = json.loads(request.body)
        # Get contents of email
        postId = data.get("id", "")

        post = Post.objects.get(id=postId)
        post.likes.add(User.objects.get(username=request.user.username))
        post.save()
        return JsonResponse({"message": "Liked successfully."}, status=201)

# API that changes the database once a posted is unliked


@csrf_exempt
def unlikePost(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    if request.method == "POST":
        data = json.loads(request.body)
        # Get contents of email
        postId = data.get("id", "")

        post = Post.objects.get(id=postId)
        post.likes.remove(User.objects.get(username=request.user.username))
        post.save()
        return JsonResponse({"message": "Unliked successfully."}, status=201)
