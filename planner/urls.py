from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("subjects/", views.subjects, name="subjects"),
    path("sessions/", views.sessions, name="sessions"),
    path("timer/<int:session_id>/", views.timer, name="timer"),
    path("api/start/", views.start_focus, name="start_focus"),
    path("api/stop/", views.stop_focus, name="stop_focus"),
    path("analytics/", views.analytics, name="analytics"),

]
