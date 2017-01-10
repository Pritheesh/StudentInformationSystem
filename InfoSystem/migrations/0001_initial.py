# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-10 17:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=128, null=True)),
                ('par_id_from_user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internal_marks', models.CharField(max_length=3)),
                ('external_marks', models.CharField(max_length=3)),
                ('results', models.CharField(max_length=5)),
                ('credits', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('hall_ticket', models.CharField(max_length=10, unique=True)),
                ('gender', models.CharField(max_length=6)),
                ('mother_name', models.CharField(max_length=128)),
                ('father_name', models.CharField(max_length=128)),
                ('student_mobile', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=128)),
                ('parent_mobile', models.CharField(max_length=15)),
                ('parent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InfoSystem.Parent')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('max_internal_marks', models.IntegerField(null=True)),
                ('max_external_marks', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='hall_ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InfoSystem.Student'),
        ),
        migrations.AddField(
            model_name='result',
            name='subject_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InfoSystem.Subject'),
        ),
    ]
