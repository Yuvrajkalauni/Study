from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("subjects/", views.subjects, name="subjects"),
    path("sessions/", views.sessions, name="sessions"),
]
