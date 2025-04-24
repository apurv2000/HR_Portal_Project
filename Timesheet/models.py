

from django.db import models

class TaskRecord(models.Model):
    task = models.ForeignKey("Project.Task", on_delete=models.CASCADE, related_name='records')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    record_name = models.CharField(max_length=255)  # This is the description
    attachment = models.FileField(upload_to='timesheet_files/', blank=True, null=True)

    def __str__(self):
        return f"{self.task.task_title} - {self.date}"
