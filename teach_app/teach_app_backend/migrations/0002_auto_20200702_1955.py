# Generated by Django 3.0.3 on 2020-07-02 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teach_app_backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=128)),
                ('date_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='teach_app_backend.Event')),
                ('specification', models.FileField(upload_to='assignments')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=3)),
            ],
            bases=('teach_app_backend.event',),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_name', models.CharField(max_length=128)),
                ('number_of_credits', models.IntegerField()),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach_app_backend.TeachUser')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission', models.FileField(upload_to='submissions')),
                ('submission_time', models.DateTimeField()),
                ('grade', models.DecimalField(decimal_places=2, max_digits=4)),
                ('feedback', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach_app_backend.TeachUser')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach_app_backend.Assignment')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach_app_backend.Unit'),
        ),
    ]
