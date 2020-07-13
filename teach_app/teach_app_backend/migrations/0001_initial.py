# Generated by Django 3.0.3 on 2020-07-13 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TeachUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('profile_picture', models.ImageField(upload_to='profile_pictures')),
                ('is_teacher', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=128)),
                ('date_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_mark', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('unit_code', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('unit_name', models.CharField(max_length=128)),
                ('unit_enrol_key', models.CharField(max_length=16)),
                ('number_of_credits', models.IntegerField()),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('unit_name', 'teacher')},
            },
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university_name', models.CharField(max_length=128, unique=True)),
                ('teacher_enrol_key', models.CharField(max_length=16)),
                ('student_enrol_key', models.CharField(max_length=16)),
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
            name='Lecture',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='teach_app_backend.Event')),
                ('link', models.CharField(max_length=128)),
            ],
            bases=('teach_app_backend.event',),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach_app_backend.Quiz')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach_app_backend.Unit'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('is_correct', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach_app_backend.Question')),
            ],
        ),
        migrations.AddField(
            model_name='teachuser',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach_app_backend.University'),
        ),
        migrations.CreateModel(
            name='UserQuizPerformance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach_app_backend.Quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'quiz')},
            },
        ),
        migrations.CreateModel(
            name='UserEnrolledUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach_app_backend.Unit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'unit')},
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach_app_backend.Answer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'answer')},
            },
        ),
        migrations.AddField(
            model_name='quiz',
            name='lecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach_app_backend.Lecture'),
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together={('unit', 'event_name')},
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission', models.FileField(upload_to='submissions')),
                ('submission_time', models.DateTimeField()),
                ('grade', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=4)),
                ('feedback', models.TextField(blank=True, default=None)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teach_app_backend.Assignment')),
            ],
            options={
                'unique_together': {('user', 'assignment')},
            },
        ),
    ]
