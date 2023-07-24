from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("taran", views.taran, name="taran"),
    path("<str:name>", views.greet, name="greet")
]