# Generated by Django 5.0.6 on 2024-09-23 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_userprofile_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='code',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
