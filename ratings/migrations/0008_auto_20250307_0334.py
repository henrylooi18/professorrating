# Generated by Django 3.2.25 on 2025-03-07 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0007_auto_20250307_0332'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
    ]
