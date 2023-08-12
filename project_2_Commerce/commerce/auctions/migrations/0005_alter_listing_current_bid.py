# Generated by Django 4.2.4 on 2023-08-06 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0004_alter_listing_category_alter_listing_current_bid_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="current_bid",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bid_listings",
                to="auctions.bid",
            ),
        ),
    ]
