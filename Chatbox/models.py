from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey("HR_App.EmployeeBISP", on_delete=models.CASCADE)
    project = models.ForeignKey("Project.Project", on_delete=models.CASCADE,null=True)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"

