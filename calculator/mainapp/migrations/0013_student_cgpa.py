# Generated by Django 3.1.7 on 2021-05-13 10:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_auto_20210513_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='cgpa',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
