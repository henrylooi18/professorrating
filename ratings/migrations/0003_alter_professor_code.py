# Generated by Django 3.2.25 on 2025-03-06 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0002_auto_20250306_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
