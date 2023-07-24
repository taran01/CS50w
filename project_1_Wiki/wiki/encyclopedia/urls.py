from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.query, name="query"),
    path("search", views.search, name="search"),
    path("newpage", views.new_page, name="newpage"),
    path("randompage", views.random_page, name="randompage"),
    path("editpage", views.edit_page, name="editpage"),
    path("savepage", views.save_page, name="savepage")
]
