# Generated by Django 3.0.7 on 2020-06-16 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0005_auto_20200616_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='my_lenta',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]