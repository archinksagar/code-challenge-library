# Generated by Django 3.2.8 on 2021-10-08 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_auto_20211008_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='due_date',
            field=models.DateField(auto_now=True),
        ),
    ]