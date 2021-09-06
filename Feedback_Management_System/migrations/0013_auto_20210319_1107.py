# Generated by Django 3.1.6 on 2021-03-19 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Feedback_Management_System', '0012_remove_descriptions_grid'),
    ]

    operations = [
        migrations.AddField(
            model_name='descriptions',
            name='grid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Griding', to='Feedback_Management_System.markinggrids'),
        ),
        migrations.AlterField(
            model_name='descriptions',
            name='criteria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Criting', to='Feedback_Management_System.assessmentcriterias'),
        ),
    ]
