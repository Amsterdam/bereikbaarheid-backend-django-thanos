# Generated by Django 4.1.10 on 2023-08-02 10:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bereikbaarheid", "0004_vma_node_view"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lastbeperking",
            name="link_nr",
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name="verkeerstelling",
            name="volg_nummer",
            field=models.IntegerField(help_text="Volgnummer", unique=True),
        ),
        migrations.AlterField(
            model_name="verrijking",
            name="link_nr",
            field=models.IntegerField(help_text="linknr", unique=True),
        ),
        migrations.AlterField(
            model_name="vma",
            name="link_nr",
            field=models.FloatField(unique=True),
        ),
    ]
