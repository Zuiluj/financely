# Generated by Django 4.2.2 on 2023-06-14 14:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_bankaccount_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
