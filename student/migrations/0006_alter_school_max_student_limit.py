# Generated by Django 3.2.13 on 2022-04-26 02:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_auto_20220426_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='max_student_limit',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
