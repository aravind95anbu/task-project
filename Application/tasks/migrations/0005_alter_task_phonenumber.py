# Generated by Django 5.0.13 on 2025-03-24 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_task_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='phonenumber',
            field=models.BigIntegerField(blank=True, null=0),
        ),
    ]
