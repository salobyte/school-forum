# Generated by Django 5.1.4 on 2025-04-07 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userContent', '0005_alter_profile_biography'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='media/avatars/'),
        ),
    ]
