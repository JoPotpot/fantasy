# Generated by Django 3.0.dev20190304153508 on 2019-08-12 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_id', models.CharField(default='', max_length=256)),
                ('name', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_id', models.CharField(default='', max_length=256)),
                ('name', models.CharField(default='', max_length=256)),
                ('player_type', models.CharField(choices=[('LB', 'Left back'), ('RB', 'Right back'), ('LW', 'Left wing'), ('RW', 'Right wing'), ('G', 'Goal keeper'), ('P', 'Pivot'), ('CB', 'Center back'), ('MG', 'Manager'), ('UK', 'Unknown')], default='UK', max_length=2)),
                ('gender', models.CharField(default='', max_length=20)),
                ('birthdate', models.DateField(null=True)),
                ('nationality', models.CharField(default='', max_length=256)),
                ('country_code', models.CharField(default='', max_length=4)),
                ('height', models.IntegerField(null=True)),
                ('weight', models.IntegerField(null=True)),
                ('jersey_number', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_id', models.CharField(default='', max_length=256)),
                ('name', models.CharField(default='', max_length=256)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('year', models.CharField(max_length=10)),
                ('competition_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Competition')),
            ],
        ),
        migrations.CreateModel(
            name='SportEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_id', models.CharField(default='', max_length=256)),
                ('home_team_score', models.IntegerField(default=0)),
                ('away_team_score', models.IntegerField(default=0)),
                ('event_date', models.DateTimeField(null=True)),
                ('start_time_confirmed', models.BooleanField(default='False')),
                ('match_status', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_id', models.CharField(default='', max_length=256)),
                ('name', models.CharField(default='', max_length=256)),
                ('country', models.CharField(default='', max_length=64)),
                ('country_code', models.CharField(default='', max_length=4)),
                ('abbreviation', models.CharField(default='', max_length=10)),
                ('manager_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Player')),
                ('season_ids', models.ManyToManyField(to='base.Season')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_id', models.CharField(default='', max_length=256)),
                ('name', models.CharField(default='', max_length=256)),
                ('city_name', models.CharField(default='', max_length=256)),
                ('country_code', models.CharField(default='', max_length=4)),
                ('country_name', models.CharField(default='', max_length=256)),
                ('capacity', models.IntegerField(null=True)),
                ('map_coordinates', models.CharField(default='', max_length=256)),
                ('team_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Team')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='venue_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Venue'),
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yellow_cards', models.IntegerField(null=True)),
                ('red_cards', models.IntegerField(null=True)),
                ('suspensions', models.IntegerField(null=True)),
                ('goals_scored', models.IntegerField(null=True)),
                ('seven_m_goals', models.IntegerField(null=True)),
                ('field_goals', models.IntegerField(null=True)),
                ('assists', models.IntegerField(null=True)),
                ('technical_fouls', models.IntegerField(null=True)),
                ('steals', models.IntegerField(null=True)),
                ('blocks', models.IntegerField(null=True)),
                ('saves', models.IntegerField(null=True)),
                ('game_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.SportEvent')),
                ('player_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Player')),
            ],
        ),
        migrations.AddField(
            model_name='sportevent',
            name='away_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='away_team', to='base.Team'),
        ),
        migrations.AddField(
            model_name='sportevent',
            name='home_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='home_team', to='base.Team'),
        ),
        migrations.AddField(
            model_name='sportevent',
            name='season_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Season'),
        ),
        migrations.AddField(
            model_name='sportevent',
            name='winner_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winner', to='base.Team'),
        ),
        migrations.AddField(
            model_name='season',
            name='team_ids',
            field=models.ManyToManyField(to='base.Team'),
        ),
        migrations.AddField(
            model_name='player',
            name='team_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Team'),
        ),
    ]
