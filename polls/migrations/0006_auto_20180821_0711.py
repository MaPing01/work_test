# Generated by Django 2.0.7 on 2018-08-21 07:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20180821_0707'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('access_role_manage', '角色管理'),),
            },
        ),
        migrations.AlterField(
            model_name='dialog',
            name='Id',
            field=models.UUIDField(default=uuid.UUID('eb3e68e8-0be1-43aa-b58d-13dc295f60b4'), editable=False, primary_key=True, serialize=False),
        ),
    ]
