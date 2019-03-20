# Generated by Django 3.0.dev20190304153508 on 2019-03-20 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0007_auto_20190318_2222'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_id', models.CharField(default='', max_length=256)),
                ('name', models.CharField(default='', max_length=256)),
                ('city_name', models.CharField(default='', max_length=256)),
                ('country_code', models.CharField(default='', max_length=4)),
                ('country_name', models.CharField(default='', max_length=256)),
                ('capacity', models.IntegerField()),
                ('map_coordinates', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.RenameModel(
            old_name='Statistics',
            new_name='Statistic',
        ),
        migrations.AddField(
            model_name='player',
            name='gender',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='player',
            name='player_type',
            field=models.CharField(choices=[('LB', 'Left back'), ('RB', 'Right back'), ('LW', 'Left wing'), ('RW', 'Right wing'), ('G', 'Goal keeper'), ('P', 'Pivot'), ('CB', 'Center back'), ('MG', 'Manager'), ('UK', 'Unknown')], default='UK', max_length=2),
        ),
    ]