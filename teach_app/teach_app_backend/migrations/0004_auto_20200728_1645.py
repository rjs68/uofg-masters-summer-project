# Generated by Django 3.0.3 on 2020-07-28 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teach_app_backend', '0003_auto_20200728_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='submission_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]