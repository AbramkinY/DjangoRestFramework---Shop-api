# Generated by Django 4.0.3 on 2022-05-31 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_created_alter_attributevalue_attribute_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
    ]