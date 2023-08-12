# Generated by Django 4.2.4 on 2023-08-06 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0003_alter_listing_current_bid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="category",
            field=models.ForeignKey(
                default="other",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="listings",
                to="auctions.category",
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="current_bid",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="bid_listings",
                to="auctions.bid",
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="img_url",
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name="listing",
            name="title",
            field=models.CharField(max_length=120),
        ),
    ]