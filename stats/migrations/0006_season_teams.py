# Generated by Django 3.0.dev20190304153508 on 2019-03-17 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0005_auto_20190313_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='teams',
            field=models.ManyToManyField(to='stats.Team'),
        ),
    ]