# Generated by Django 3.1.7 on 2021-03-24 04:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20210323_2142'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('username', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.CreateModel(
            name='FacultyCourse',
            fields=[
                ('course_title', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('year', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.faculty')),
            ],
        ),
    ]
