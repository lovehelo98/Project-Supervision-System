# Generated by Django 3.1.6 on 2021-03-19 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Feedback_Management_System', '0011_auto_20210319_1026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='descriptions',
            name='grid',
        ),
    ]