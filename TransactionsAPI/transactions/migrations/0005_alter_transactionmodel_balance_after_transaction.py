# Generated by Django 3.2.7 on 2021-09-17 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_alter_transactionmodel_balance_after_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionmodel',
            name='balance_after_transaction',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
