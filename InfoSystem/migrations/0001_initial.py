# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-25 13:56
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AchievementInASemester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AchievementInASubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('year_of_pursue_roman', models.CharField(max_length=5)),
                ('semester_roman', models.CharField(max_length=2)),
                ('semester', models.IntegerField()),
                ('year_of_pursue', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='ExamInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_of_pursue_roman', models.CharField(max_length=5)),
                ('semester_roman', models.CharField(max_length=2)),
                ('year_of_pursue', models.IntegerField()),
                ('semester', models.IntegerField()),
                ('year_of_calendar', models.IntegerField()),
                ('month_of_year', models.CharField(max_length=15)),
                ('supple', models.BooleanField()),
                ('total', models.CharField(default='0', max_length=3)),
            ],
            options={
                'ordering': ['year_of_pursue', 'semester'],
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mother_name', models.CharField(max_length=128)),
                ('father_name', models.CharField(max_length=128)),
                ('mobile', models.CharField(max_length=15, null=True)),
                ('email', models.CharField(max_length=128, null=True)),
                ('is_registered', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internal_marks', models.CharField(max_length=3)),
                ('external_marks', models.CharField(max_length=3)),
                ('total', models.CharField(max_length=3)),
                ('results', models.CharField(max_length=5)),
                ('credits', models.IntegerField()),
                ('examinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result', to='InfoSystem.ExamInfo')),
            ],
        ),
        migrations.CreateModel(
            name='SaltForActivation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('hall_ticket', models.CharField(max_length=10, unique=True)),
                ('gender', models.CharField(max_length=6)),
                ('mobile', models.CharField(max_length=15, null=True)),
                ('email', models.CharField(max_length=128, null=True)),
                ('is_registered', models.BooleanField(default=False)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InfoSystem.Branch')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InfoSystem.Parent')),
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
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('mobile', models.CharField(max_length=15)),
                ('is_student', models.BooleanField(default=False, verbose_name='Student')),
                ('is_verified', models.BooleanField(default=False, verbose_name='verified')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='saltforactivation',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='result',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='InfoSystem.Subject'),
        ),
        migrations.AddField(
            model_name='parent',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='examinfo',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examinfo', to='InfoSystem.Student'),
        ),
        migrations.AddField(
            model_name='achievementinasubject',
            name='result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ach_res', to='InfoSystem.Result'),
        ),
        migrations.AddField(
            model_name='achievementinasubject',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ach_subject', to='InfoSystem.Student'),
        ),
        migrations.AddField(
            model_name='achievementinasemester',
            name='examinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examinfo', to='InfoSystem.ExamInfo'),
        ),
        migrations.AddField(
            model_name='achievementinasemester',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievementinasemester', to='InfoSystem.Student'),
        ),
    ]
