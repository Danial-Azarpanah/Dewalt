# Generated by Django 4.0 on 2023-07-03 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_picture_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='proper_tools',
            field=models.ManyToManyField(blank=True, null=True, related_name='proper_tools', to='product.Product', verbose_name='ابزارهای مناسب'),
        ),
    ]
