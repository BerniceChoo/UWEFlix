from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cust', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='showings',
            name='sociallyDistanced',
            field=models.BooleanField(default=False),
        ),
    ]
