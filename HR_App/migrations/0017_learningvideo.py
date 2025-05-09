# Generated by Django 5.2 on 2025-04-24 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0016_alter_leave_half_day_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('section', models.CharField(choices=[('Project Management', 'Project Management'), ('Timesheet Management', 'Timesheet Management'), ('Leave Management', 'Leave Management')], max_length=50)),
                ('video', models.FileField(upload_to='learning_videos/')),
            ],
        ),
    ]
