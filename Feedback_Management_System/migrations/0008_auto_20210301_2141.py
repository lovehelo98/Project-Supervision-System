# Generated by Django 3.1.6 on 2021-03-01 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Feedback_Management_System', '0007_auto_20210301_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marks',
            name='criteria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='crt', to='Feedback_Management_System.assessmentcriterias'),
        ),
    ]
