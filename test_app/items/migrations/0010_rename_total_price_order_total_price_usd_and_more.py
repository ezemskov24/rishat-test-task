# Generated by Django 5.0.2 on 2024-02-28 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0009_alter_order_total_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_price',
            new_name='total_price_usd',
        ),
        migrations.AddField(
            model_name='order',
            name='total_price_eur',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
