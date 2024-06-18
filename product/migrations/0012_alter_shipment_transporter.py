# Generated by Django 5.0 on 2024-05-28 04:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_alter_shipment_customer_alter_shipment_transporter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='transporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.transporter'),
        ),
    ]