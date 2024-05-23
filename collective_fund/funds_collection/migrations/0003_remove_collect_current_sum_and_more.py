# Generated by Django 5.0.6 on 2024-05-22 06:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funds_collection', '0002_alter_collect_options_alter_payment_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collect',
            name='current_sum',
        ),
        migrations.RemoveField(
            model_name='collect',
            name='people_amount',
        ),
        migrations.AlterField(
            model_name='collect',
            name='target_sum',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(1.0)], verbose_name='Сумма сбора'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='donation_sum',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(1.0)], verbose_name='Сумма пожертвования'),
        ),
    ]
