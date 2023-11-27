# Generated by Django 4.2.7 on 2023-11-27 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='time_stamp',
            field=models.TimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='history',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='search_click',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='search_click',
            name='time_stamp',
            field=models.TimeField(auto_now=True, null=True),
        ),
    ]
