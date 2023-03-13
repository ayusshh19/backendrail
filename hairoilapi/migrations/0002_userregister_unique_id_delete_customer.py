# Generated by Django 4.1 on 2023-03-10 19:06

from django.db import migrations, models
import hairoilapi.models


class Migration(migrations.Migration):

    dependencies = [
        ('hairoilapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregister',
            name='unique_id',
            field=models.UUIDField(default=hairoilapi.models.generate_uuid, editable=False, unique=True),
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
