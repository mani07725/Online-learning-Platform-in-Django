# Generated by Django 4.2.1 on 2023-06-10 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0006_course_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='Type',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
