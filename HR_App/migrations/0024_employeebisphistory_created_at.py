# Generated by Django 5.2 on 2025-05-06 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0023_employeebisp_reported_to_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeebisphistory',
            name='created_at',
            field=models.DateTimeField(null=True),
        ),
    ]
