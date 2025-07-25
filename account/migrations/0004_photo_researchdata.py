# Generated by Django 5.1.5 on 2025-05-18 10:31

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_evcharginglocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='photos/')),
            ],
        ),
        migrations.CreateModel(
            name='ResearchData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('crop_type', models.CharField(blank=True, max_length=100, null=True)),
                ('soil_data', models.JSONField(blank=True, null=True)),
                ('soil_raster', models.FileField(blank=True, null=True, upload_to='soil_rasters/')),
                ('date_collected', models.DateField()),
                ('researcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_za_utafiti', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
