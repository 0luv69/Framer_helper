# Generated by Django 5.0.6 on 2024-05-29 13:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_email_verified', models.BooleanField(default=False)),
                ('email_token', models.CharField(blank=True, max_length=100, null=True)),
                ('user_m', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FramerUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Bio', models.TextField(default='Hey, I am Framer Here')),
                ('profile_img', models.ImageField(blank=True, null=True, upload_to='profile_pic')),
                ('ph_num', models.IntegerField(blank=True, null=True)),
                ('trust_rate', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1)),
                ('Profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authenticate.profile')),
            ],
        ),
        migrations.CreateModel(
            name='BuyerUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_img', models.ImageField(blank=True, null=True, upload_to='profile_pic')),
                ('ph_num', models.IntegerField(blank=True, null=True)),
                ('Profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authenticate.profile')),
            ],
        ),
    ]
