# Generated by Django 3.1.7 on 2021-05-18 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0004_auto_20210509_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='results',
            field=models.TextField(max_length=500, null=True),
        ),
    ]