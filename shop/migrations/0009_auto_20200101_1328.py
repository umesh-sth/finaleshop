# Generated by Django 2.2.7 on 2020-01-01 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20200101_1327'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Orders',
            new_name='Order',
        ),
    ]
