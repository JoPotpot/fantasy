# Generated by Django 3.0.dev20190304153508 on 2019-03-26 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0015_auto_20190326_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='venue_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stats.Venue'),
        ),
    ]