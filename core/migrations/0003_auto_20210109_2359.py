# Generated by Django 3.1.5 on 2021-01-09 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210109_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='matric',
            field=models.CharField(max_length=10),
        ),
    ]
