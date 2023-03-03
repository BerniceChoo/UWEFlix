# Generated by Django 4.0.8 on 2023-01-15 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='club',
            old_name='emp_email',
            new_name='club_email',
        ),
        migrations.AddField(
            model_name='club',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
