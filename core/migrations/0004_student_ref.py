# Generated by Django 3.1.5 on 2021-01-10 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210109_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='ref',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]
