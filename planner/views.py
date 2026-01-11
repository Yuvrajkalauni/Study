from django.shortcuts import render
form django.contrib.auth.decorators import login_required
from .models import Subject, StudySession
# Create your views here.

@login_required
def dashboard(request):
    subjects = Subject.objects.filter(user=request.user)
    sessions = StudySession.objects.filter(user=request.user)

    context = {
        "subjects": subjects,
        "sessions": sessions
    }
    return render(request, "dashboard.html", context)


@login_required
def subjects(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Subject.objects.create(
                user=request.user,
                name=name
            )

    subjects = Subject.objects.filter(user=request.user)
    return render(request, "subjects.html", {
        "subjects": subjects
    })

@login_required
def sessions(request):
    subjects = Subject.objects.filter(user=request.user)

    if request.method == "POST":
        subject_id = request.POST.get("subject")
        duration = request.POST.get("duration")
        date = request.POST.get("date")

        if subject_id and duration and date:
            StudySession.objects.create(
                user=request.user,
                subject_id=subject_id,
                planned_duration=duration,
                date=date
            )

    sessions = StudySession.objects.filter(user=request.user)

    return render(request, "sessions.html", {
        "sessions": sessions,
        "subjects": subjects
    })

