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
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.Foreignkey(Subject,on_delete=models.CASCADE)
    planned_duration = models.Integerfield()
    actual_duration = models.IntegerField(Default=0)
    data = models.DateField()
    complete = models.BooleanField(default=false)

    def __str__(self):
        return f"{self.objects.name} = {self.data}"
    
class FocusLog(models.Model):
    session = models.Foreginkey(StudySession,on_delete=models.CASCADE)
    start_time = models.DateField()
    end_time = models.DateField(null=True, blank=False)
