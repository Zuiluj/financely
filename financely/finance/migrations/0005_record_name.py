# Generated by Django 4.2.2 on 2023-06-14 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_bankaccount_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='name',
            field=models.CharField(default='Record', max_length=200),
        ),
    ]
