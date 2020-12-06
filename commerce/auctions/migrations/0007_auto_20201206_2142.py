# Generated by Django 3.1.3 on 2020-12-06 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='create_listing',
            name='Category',
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=64)),
                ('cat_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.create_listing')),
                ('cat_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['category'],
            },
        ),
    ]
