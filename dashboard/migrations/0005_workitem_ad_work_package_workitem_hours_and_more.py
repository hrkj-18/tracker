# Generated by Django 4.0.5 on 2022-06-30 07:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_workitem_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='workitem',
            name='ad_work_package',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='workitem',
            name='hours',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='workitem',
            name='in_DM',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 30, 12, 34, 14, 395735)),
        ),
    ]