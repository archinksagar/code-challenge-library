# Generated by Django 3.2.8 on 2021-10-08 23:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_transaction_due_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='due_date',
        ),
    ]