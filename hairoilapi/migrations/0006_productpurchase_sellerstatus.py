# Generated by Django 4.1 on 2023-03-13 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hairoilapi', '0005_userregister_issseller'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpurchase',
            name='sellerstatus',
            field=models.BooleanField(default=False),
        ),
    ]
