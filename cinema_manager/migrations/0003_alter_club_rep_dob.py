# Generated by Django 4.0.8 on 2023-01-15 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_manager', '0002_rename_emp_email_club_club_email_club_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='rep_dob',
            field=models.CharField(max_length=8),
        ),
    ]
