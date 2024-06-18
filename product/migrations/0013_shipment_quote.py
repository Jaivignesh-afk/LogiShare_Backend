# Generated by Django 5.0 on 2024-05-29 03:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_alter_shipment_transporter'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='quote',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipment_quote', to='product.transporter'),
        ),
    ]