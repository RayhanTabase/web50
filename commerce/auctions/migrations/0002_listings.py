# Generated by Django 3.0.5 on 2020-10-16 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=30)),
                ('item_description', models.CharField(max_length=1000)),
                ('bid_price', models.IntegerField()),
            ],
        ),
    ]
