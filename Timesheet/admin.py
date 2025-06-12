from django.contrib import admin

from .models import TaskRecord, ImagetaskRecord

# Register your models here.
admin.site.register(TaskRecord)
admin.site.register(ImagetaskRecord)

