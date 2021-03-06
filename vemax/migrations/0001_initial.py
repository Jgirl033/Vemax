# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-06 14:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classify',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('class_name', models.CharField(max_length=10)),
                ('img_url', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_friend', models.CharField(max_length=5000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('image_url', models.URLField()),
                ('sex', models.CharField(max_length=5)),
                ('birthday', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=100)),
                ('intro', models.TextField()),
                ('tags', models.CharField(max_length=100)),
                ('work_experience', models.TextField(null=True)),
                ('study_experience', models.TextField()),
                ('user_degree', models.CharField(max_length=5)),
                ('user_class', models.CharField(max_length=50)),
                ('class_tags', models.CharField(max_length=50, null=True)),
                ('is_organization', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Profiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.CharField(max_length=10)),
                ('content', models.TextField()),
                ('time', models.DateField()),
                ('like_count', models.IntegerField()),
                ('forward_count', models.IntegerField()),
                ('comment_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_uid', models.CharField(max_length=15)),
                ('relationship', models.CharField(max_length=20)),
                ('degree', models.FloatField()),
                ('is_follow', models.BooleanField(default=False)),
                ('is_fans', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('username', models.CharField(max_length=50, null=True)),
                ('uid', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('pwd', models.CharField(max_length=20)),
                ('is_register', models.BooleanField(default=False)),
                ('is_crawler', models.BooleanField(default=False)),
                ('is_classify', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='userrelationship',
            name='user_uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vemax.Users'),
        ),
        migrations.AddField(
            model_name='profiles',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vemax.Users'),
        ),
        migrations.AddField(
            model_name='information',
            name='uid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='vemax.Users'),
        ),
        migrations.AddField(
            model_name='friend',
            name='uid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='vemax.Users'),
        ),
        migrations.AlterUniqueTogether(
            name='userrelationship',
            unique_together=set([('user_uid', 'friend_uid')]),
        ),
        migrations.AlterUniqueTogether(
            name='profiles',
            unique_together=set([('uid', 'cid')]),
        ),
    ]
