# Generated by Django 5.1.5 on 2025-04-08 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_account_first_name_account_groups_account_last_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EVChargingLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_name', models.CharField(max_length=250)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
    ]
