# Generated by Django 3.2.8 on 2021-10-08 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_remove_transaction_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='due_date',
            field=models.DateField(default='2021-10-08'),
            preserve_default=False,
        ),
    ]
