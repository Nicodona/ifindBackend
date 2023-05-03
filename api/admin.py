from django.contrib import admin
from .models import Register, Found, Job, Report, Message

admin.site.register(Register)
admin.site.register(Found)
admin.site.register(Job)
admin.site.register(Report)
admin.site.register(Message)