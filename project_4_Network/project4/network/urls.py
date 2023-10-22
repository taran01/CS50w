
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.new_post, name="new_post"),
    path("following", views.following, name="following"),

    # APIs
    path("edit", views.edit_post, name="edit_post"),
    path("change-follow", views.change_follow, name="change_follow"),
    path("change-like", views.change_like, name="change-like"),

    # User-profile
    path("<str:username>", views.profile_page, name="profile_page")
]
