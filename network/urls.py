
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.newPost, name="newPost"),
    path("/<str:username>", views.viewUsername, name="viewUsername"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow"),
    path("following", views.following, name="followingPage"),

    # API
    path("editPost/<int:id>", views.editPost, name="editPost"),
    path("likePost/<int:id>", views.likePost, name="likePost"),
    path("unlikePost/<int:id>", views.unlikePost, name="unlikePost")
]
