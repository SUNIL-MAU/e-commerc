# Generated by Django 3.1.2 on 2020-11-22 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='conform_password',
            field=models.CharField(default='', max_length=500),
        ),
    ]
