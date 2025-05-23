

from django.db import models




class Project(models.Model):
    RATE_STATUS_CHOICES = [
        ('Billable', 'Billable'),
        ('Non Billable', 'Non Billable'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    project_name = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200, blank=True, null=True)

    start_date = models.DateField()
    end_date = models.DateField()

    rate_status = models.CharField(max_length=20, choices=RATE_STATUS_CHOICES, default='Non Billable')
    rate_currency = models.CharField(max_length=10, default='Rs')  # Optional: could be a dropdown
    rate_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')

    leader = models.ForeignKey("HR_App.EmployeeBISP", on_delete=models.SET_NULL, related_name='leading_projects', null=True, )
    admin = models.ForeignKey("HR_App.EmployeeBISP", on_delete=models.SET_NULL, related_name='admin_projects', null=True, )

    team_members = models.ManyToManyField("HR_App.EmployeeBISP", related_name='project_team')

    description = models.TextField()
    upload_file = models.FileField(upload_to='project_files/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    version = models.IntegerField(default=1)
    status = models.CharField(max_length=20, default="active")  # 'active' or 'inactive'
    timestamp = models.DateTimeField(auto_now=True)

    def soft_delete(self):
        """Mark the project as deleted (soft delete)."""
        self.status = 'Inactive'
        self.save()

    def save(self, *args, **kwargs):
        if self.pk:  # existing record
            self.version += 1
        super().save(*args, **kwargs)

    @property
    def model_name(self):
        return 'project'


    def __str__(self):
        return self.project_name

# For Versioning
class ProjectHistory(models.Model):
    project = models.ForeignKey(Project, related_name='history', on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    rate_status = models.CharField(max_length=20, choices=Project.RATE_STATUS_CHOICES)
    rate_currency = models.CharField(max_length=10)
    rate_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    priority = models.CharField(max_length=10, choices=Project.PRIORITY_CHOICES)
    leader = models.ForeignKey("HR_App.EmployeeBISP", on_delete=models.SET_NULL, null=True, related_name='+')
    admin = models.ForeignKey("HR_App.EmployeeBISP", on_delete=models.SET_NULL, null=True, related_name='+')
    team_members = models.ManyToManyField("HR_App.EmployeeBISP", related_name='team')
    description = models.TextField()
    upload_file = models.FileField(upload_to='project_files/', blank=True, null=True)
    version = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"History for {self.project.project_name} - Version {self.version}"

    @property
    def model_name(self):
        return 'projecthistory'


class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Inprogress', 'Inprogress'),
        ('Claimed Completed', 'Claimed Completed'),
        ('Completed', 'Completed'),
        ('On Hold','On Hold')
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    task_title = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    start_date = models.DateField()
    end_date = models.DateField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')

    assigned_to = models.ForeignKey("HR_App.EmployeeBISP", on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')

    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    version = models.IntegerField(default=1)
    status_field = models.CharField(max_length=20, default="active")  # 'active' or 'inactive'
    timestamp = models.DateTimeField(auto_now=True)

    def soft_delete(self):
        """Mark the project as deleted (soft delete)."""
        self.status = 'Inactive'
        self.save()

    def save(self, *args, **kwargs):
        if self.pk:  # existing record
            self.version += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.task_title

class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='history')
    task_title = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20)
    priority = models.CharField(max_length=10)
    assigned_to = models.ForeignKey("HR_App.EmployeeBISP", on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    version = models.IntegerField(default=1)  # Version number
    status_field= models.CharField(max_length=20, default='active')  # New status field (active/inactive)
    timestamp = models.DateTimeField(auto_now=True)  # Timestamp for when the history was created
    created_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"History of {self.task_title} (Version {self.version})"

    class Meta:
        ordering = ['-timestamp']  # Order by timestamp in reverse to get latest first
