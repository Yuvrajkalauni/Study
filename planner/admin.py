from django.contrib import admin
from .models import Subject, StudySession, FocusLog

admin.site.register(Subject)
admin.site.register(StudySession)
admin.site.register(FocusLog)
