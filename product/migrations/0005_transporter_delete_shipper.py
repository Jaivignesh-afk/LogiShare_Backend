# Generated by Django 5.0 on 2024-05-27 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_remove_shipper_offer_price_shipment_offer_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transporter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('display_name', models.CharField(max_length=100)),
                ('password_hash', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=10)),
                ('token', models.CharField(max_length=100)),
                ('company_name', models.CharField(default='dummy', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Shipper',
        ),
    ]