# Generated by Django 4.1 on 2023-03-13 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hairoilapi', '0009_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='prodid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='hairoilapi.productpurchase'),
        ),
        migrations.AddField(
            model_name='order',
            name='userid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='hairoilapi.userregister'),
        ),
    ]