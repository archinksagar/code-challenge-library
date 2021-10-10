# Generated by Django 3.2.8 on 2021-10-08 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='return_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='library_returned',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transactions_returned', to='library.library'),
        ),
    ]
