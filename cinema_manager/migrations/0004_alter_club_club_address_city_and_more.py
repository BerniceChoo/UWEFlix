# Generated by Django 4.0.8 on 2023-01-15 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_manager', '0003_alter_club_rep_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='club_address_city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='club',
            name='club_address_number',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='club',
            name='club_address_postcode',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='club',
            name='club_address_street',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='club',
            name='club_email',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='club',
            name='club_phone',
            field=models.IntegerField(max_length=10),
        ),
        migrations.AlterField(
            model_name='club',
            name='club_tphone',
            field=models.IntegerField(max_length=10),
        ),
        migrations.AlterField(
            model_name='club',
            name='rep_dob',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='club',
            name='rep_first_name',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='club',
            name='rep_last_name',
            field=models.CharField(max_length=30),
        ),
    ]
