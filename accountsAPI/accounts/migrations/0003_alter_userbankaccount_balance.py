# Generated by Django 3.2.7 on 2021-09-16 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbankaccount',
            name='balance',
            field=models.CharField(max_length=12),
        ),
    ]