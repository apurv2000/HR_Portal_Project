# Generated by Django 5.2 on 2025-04-21 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_App', '0014_leavetype_is_deleted_leavetype_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavetype',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('hidden', 'Hidden'), ('delete', 'Delete')], default='active', max_length=10),
        ),
    ]
