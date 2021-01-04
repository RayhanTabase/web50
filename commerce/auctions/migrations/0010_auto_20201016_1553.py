# Generated by Django 3.0.5 on 2020-10-16 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20201016_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=30)),
                ('cmt_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Cmts', to='auctions.Listing')),
            ],
        ),
        migrations.DeleteModel(
            name='Cmts',
        ),
    ]
