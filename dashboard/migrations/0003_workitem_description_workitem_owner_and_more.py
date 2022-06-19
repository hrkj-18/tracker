# Generated by Django 4.0.5 on 2022-06-18 18:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_comment_options_workitem_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='workitem',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='workitem',
            name='owner',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='workitem',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 19, 0, 22, 41, 50911)),
        ),
    ]
