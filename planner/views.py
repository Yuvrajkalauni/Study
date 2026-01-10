from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Subject, StudySession
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from .models import FocusLog, StudySession
from django.db.models import Sum, F, ExpressionWrapper, DurationField

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


def test_template(request):
    return render(request, "registration/login.html")


@login_required
def timer(request, session_id):
    session = StudySession.objects.get(id=session_id, user=request.user)
    return render(request, "timer.html", {"session": session})


@login_required
@csrf_exempt
def start_focus(request):
    if request.method == "POST":
        session_id = request.POST.get("session_id")
        session = StudySession.objects.get(id=session_id, user=request.user)

        log = FocusLog.objects.create(
            session=session,
            start_time=now()
        )

        return JsonResponse({"log_id": log.id})

@login_required
@csrf_exempt
def stop_focus(request):
    if request.method == "POST":
        log_id = request.POST.get("log_id")

        log = FocusLog.objects.get(id=log_id)
        log.end_time = now()
        log.save()

        return JsonResponse({"status": "stopped"})


@login_required
def analytics(request):
    logs = FocusLog.objects.filter(
        session__user=request.user,
        end_time__isnull=False
    )

    duration_expr = ExpressionWrapper(
        F("end_time") - F("start_time"),
        output_field=DurationField()
    )

    logs = logs.annotate(duration=duration_expr)

    subject_totals = {}

    for log in logs:
        subject = log.session.subject.name
        seconds = log.duration.total_seconds()
        subject_totals[subject] = subject_totals.get(subject, 0) + seconds

    labels = list(subject_totals.keys())
    values = [v / 60 for v in subject_totals.values()]  # minutes

    return render(request, "analytics.html", {
        "labels": labels,
        "values": values
    })

