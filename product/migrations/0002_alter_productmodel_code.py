# Generated by Django 4.2 on 2023-04-08 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='code',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
