# Generated by Django 2.2.7 on 2020-01-01 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_order_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='del_address',
            field=models.CharField(default='', max_length=64),
        ),
    ]