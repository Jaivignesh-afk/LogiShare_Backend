# Generated by Django 5.0 on 2024-05-24 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='offer_price',
            field=models.IntegerField(blank=True, default=1000),
        ),
    ]