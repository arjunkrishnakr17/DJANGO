# Generated by Django 4.2.1 on 2023-06-24 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_customer_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='password',
        ),
    ]
