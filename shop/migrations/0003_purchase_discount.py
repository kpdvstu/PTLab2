# Generated by Django 3.2.8 on 2021-10-23 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_purchase_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='discount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=3),
        ),
    ]
