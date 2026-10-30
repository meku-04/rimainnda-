
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("delete/<int:id>/", views.delete_task, name="delete"),
    path("edit/<int:id>/", views.edit_task, name="edit"),
    path("toggle/<int:id>/", views.toggle_task, name="toggle"),
]
