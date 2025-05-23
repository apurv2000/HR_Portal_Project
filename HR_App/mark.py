from django.utils import timezone
from .models import ResignationApplication

def mark_resigned_employees_inactive():
    today = timezone.now().date()
    resignations = ResignationApplication.objects.filter(last_working_date__lt=today)
    updated = 0

    for resignation in resignations:
        employee = resignation.employee
        if employee.status != 'inactive':
            employee.status = 'inactive'
            employee.save()
            updated += 1

    return updated


