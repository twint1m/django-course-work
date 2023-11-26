# Generated by Django 4.1.1 on 2023-06-27 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0013_remove_stock_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webshop.product', verbose_name='Product')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webshop.stock', verbose_name='Stock')),
            ],
            options={
                'verbose_name': 'Product Stock',
                'verbose_name_plural': 'Product Stocks',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_stock',
            field=models.ManyToManyField(related_name='products', through='webshop.ProductStock', to='webshop.stock', verbose_name='Stocks'),
        ),
    ]