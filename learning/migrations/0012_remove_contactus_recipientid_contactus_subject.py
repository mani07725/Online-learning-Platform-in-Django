# Generated by Django 4.2.1 on 2023-06-12 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0011_alter_trainerinfo_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactus',
            name='RecipientID',
        ),
        migrations.AddField(
            model_name='contactus',
            name='Subject',
            field=models.CharField(default='', max_length=50),
        ),
    ]