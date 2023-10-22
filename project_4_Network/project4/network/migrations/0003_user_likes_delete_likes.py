# Generated by Django 4.2.4 on 2023-09-20 12:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0002_post_likes_followers"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="likes",
            field=models.ManyToManyField(related_name="user_likes", to="network.post"),
        ),
        migrations.DeleteModel(
            name="Likes",
        ),
    ]