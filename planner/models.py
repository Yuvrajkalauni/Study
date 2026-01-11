from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default="blue")

    def __str__(self):
        return self.name

    
class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    planned_duration = models.IntegerField()  # minutes
    actual_duration = models.IntegerField(default=0)
    date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject.name} - {self.date}"

    
class FocusLog(models.Model):
    session = models.ForeignKey(StudySession, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

