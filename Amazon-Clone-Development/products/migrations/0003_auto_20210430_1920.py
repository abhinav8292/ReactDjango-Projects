# Generated by Django 3.1.2 on 2021-04-30 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_orders_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='timestamp',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
