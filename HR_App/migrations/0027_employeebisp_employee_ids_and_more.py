# Generated by Django 5.2 on 2025-05-13 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0026_resignationapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeebisp',
            name='employee_IDs',
            field=models.CharField(blank=True, editable=False, max_length=20, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='employeebisphistory',
            name='employee_IDs',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
