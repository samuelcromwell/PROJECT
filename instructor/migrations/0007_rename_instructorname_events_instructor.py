# Generated by Django 5.0.2 on 2024-02-29 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instructor', '0006_rename_instructor_events_instructorname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='events',
            old_name='instructorname',
            new_name='instructor',
        ),
    ]