# Generated by Django 3.1.5 on 2021-01-09 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ('-created',)},
        ),
        migrations.RenameField(
            model_name='student',
            old_name='number',
            new_name='phone',
        ),
    ]
