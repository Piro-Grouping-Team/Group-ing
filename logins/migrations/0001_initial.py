# Generated by Django 4.1 on 2022-08-09 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, verbose_name='이메일')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=20, verbose_name='이름')),
                ('nickname', models.CharField(max_length=20, null=True, unique=True, verbose_name='닉네임')),
                ('age', models.IntegerField(null=True, verbose_name='나이')),
                ('address', models.CharField(max_length=100, verbose_name='주소')),
                ('addressDetail', models.CharField(max_length=100, verbose_name='상세주소')),
                ('gender', models.CharField(choices=[('male', '남성'), ('female', '여성'), ('None', '선택안함')], max_length=10, verbose_name='성별')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
