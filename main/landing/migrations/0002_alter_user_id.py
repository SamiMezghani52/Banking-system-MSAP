# Generated by Django 3.2.7 on 2021-09-17 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True),
        ),
    ]
