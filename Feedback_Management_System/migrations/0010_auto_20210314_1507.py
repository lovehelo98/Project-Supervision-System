# Generated by Django 3.1.6 on 2021-03-14 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Feedback_Management_System', '0009_auto_20210308_1957'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='descriptions',
            options={'ordering': ['descp']},
        ),
    ]