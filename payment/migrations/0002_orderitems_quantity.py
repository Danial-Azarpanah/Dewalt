# Generated by Django 4.2.1 on 2023-06-13 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]