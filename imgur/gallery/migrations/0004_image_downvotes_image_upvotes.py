# Generated by Django 5.0.7 on 2024-07-21 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_post_alter_user_options_user_date_joined_user_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='downvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='image',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
    ]
