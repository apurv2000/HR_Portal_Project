# Generated by Django 5.2 on 2025-04-23 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0015_alter_leavetype_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='half_day_type_name',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
