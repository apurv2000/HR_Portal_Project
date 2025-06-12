from django.contrib import admin


from .models import ProjectHistory, Task, TaskHistory,Project

# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectHistory)
admin.site.register(Task)
admin.site.register(TaskHistory)

