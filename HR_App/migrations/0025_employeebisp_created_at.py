# Generated by Django 5.2 on 2025-05-06 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0024_employeebisphistory_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeebisp',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
