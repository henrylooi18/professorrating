# Generated by Django 3.2.25 on 2025-03-06 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='professor',
            name='code',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
