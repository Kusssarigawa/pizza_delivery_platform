# Generated by Django 5.0.4 on 2024-11-09 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_rename_product_id_orderitem_object_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_address',
        ),
    ]
