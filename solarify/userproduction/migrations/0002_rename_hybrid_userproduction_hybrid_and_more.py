# Generated by Django 4.1.3 on 2022-11-30 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userproduction', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userproduction',
            old_name='Hybrid',
            new_name='hybrid',
        ),
        migrations.RenameField(
            model_name='userproduction',
            old_name='amount',
            new_name='power',
        ),
    ]