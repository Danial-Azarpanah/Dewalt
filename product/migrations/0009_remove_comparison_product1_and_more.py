# Generated by Django 4.2.1 on 2023-07-08 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_remove_discountcode_product_discountcode_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comparison',
            name='product1',
        ),
        migrations.RemoveField(
            model_name='comparison',
            name='product2',
        ),
        migrations.AddField(
            model_name='comparison',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comparison', to='product.product', verbose_name='کالای اول'),
        ),
    ]
