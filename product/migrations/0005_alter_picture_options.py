# Generated by Django 4.2.1 on 2023-07-03 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_features'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='picture',
            options={'ordering': ('id',), 'verbose_name': 'تصویر محصول', 'verbose_name_plural': 'تصویر محصول'},
        ),
    ]