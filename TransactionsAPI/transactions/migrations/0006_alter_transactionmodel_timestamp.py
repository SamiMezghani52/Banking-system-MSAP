# Generated by Django 3.2.7 on 2021-09-17 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_alter_transactionmodel_balance_after_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionmodel',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
