# Generated by Django 3.0.5 on 2020-10-16 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_cmts_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cmts',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.Listing'),
        ),
    ]
