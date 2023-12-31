# Generated by Django 4.1.9 on 2023-06-26 14:33

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Gebied",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("geom", django.contrib.gis.db.models.fields.PolygonField(srid=28992)),
            ],
            options={
                "verbose_name": "Gebied",
                "verbose_name_plural": "Gebieden",
            },
        ),
        migrations.CreateModel(
            name="Lastbeperking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("link_nr", models.IntegerField()),
                ("lastbeperking_in_kg", models.FloatField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Lastbeperking",
                "verbose_name_plural": "Lastbeperkingen",
            },
        ),
        migrations.CreateModel(
            name="Stremming",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("link_nr", models.IntegerField(db_index=True, help_text="vma_linknr")),
                ("werkzaamheden", models.CharField(max_length=255)),
                ("opmerking", models.CharField(blank=True, max_length=1000, null=True)),
                ("kenmerk", models.CharField(blank=True, max_length=255, null=True)),
                ("url", models.CharField(blank=True, max_length=255, null=True)),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
            ],
            options={
                "verbose_name": "Stremming",
                "verbose_name_plural": "Stremmingen",
            },
        ),
        migrations.CreateModel(
            name="VenstertijdWeg",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("link_nr", models.IntegerField(help_text="linknr")),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("e_type", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "verkeersbord",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "dagen",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            blank=True, max_length=10, null=True
                        ),
                        size=None,
                    ),
                ),
                ("begin_tijd", models.TimeField(blank=True, null=True)),
                ("eind_tijd", models.TimeField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Venstertijdweg",
                "verbose_name_plural": "Venstertijdwegen",
            },
        ),
        migrations.CreateModel(
            name="VerkeersBord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bord_id", models.IntegerField(unique=True)),
                ("geldigheid", models.CharField(max_length=99)),
                ("rvv_modelnummer", models.CharField(max_length=25)),
                ("tekst", models.CharField(blank=True, max_length=25, null=True)),
                ("kijkrichting", models.IntegerField()),
                ("link_nr", models.IntegerField(help_text="script_link_nr")),
                ("link_gevalideerd", models.IntegerField()),
                ("tekst_waarde", models.FloatField(blank=True, null=True)),
                (
                    "onderbord_tekst",
                    models.CharField(blank=True, max_length=299, null=True),
                ),
                (
                    "verkeersbesluit",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("versie", models.DateField()),
                ("rd_x", models.IntegerField()),
                ("rd_y", models.IntegerField()),
                ("link_validated_2", models.IntegerField()),
                ("panorama", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "geometry",
                    django.contrib.gis.db.models.fields.PointField(
                        blank=True, srid=28992
                    ),
                ),
            ],
            options={
                "verbose_name": "Verkeersbord",
                "verbose_name_plural": "Verkeersborden",
            },
        ),
        migrations.CreateModel(
            name="VerkeersPaal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("link_nr", models.IntegerField(help_text="linknr")),
                (
                    "paal_nr",
                    models.CharField(
                        blank=True, help_text="paalnummer", max_length=255, null=True
                    ),
                ),
                (
                    "verkeersbord",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "dagen",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=10), size=None
                    ),
                ),
                ("begin_tijd", models.TimeField()),
                ("eind_tijd", models.TimeField()),
                (
                    "geometry",
                    django.contrib.gis.db.models.fields.PointField(srid=28992),
                ),
                ("type", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "standplaats",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("jaar_aanleg", models.IntegerField(blank=True, null=True)),
                (
                    "venstertijden",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "toegangssysteem",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("camera", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "beheerorganisatie",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "bijzonderheden",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
            ],
            options={
                "verbose_name": "Verkeerspaal",
                "verbose_name_plural": "Verkeerspalen",
            },
        ),
        migrations.CreateModel(
            name="VerkeersTelling",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("volg_nummer", models.IntegerField(help_text="Volgnummer")),
                ("lat", models.FloatField(help_text="Latitude")),
                ("lon", models.FloatField(help_text="Longitude")),
                (
                    "link_nr",
                    models.IntegerField(blank=True, help_text="vma_link_nr", null=True),
                ),
                ("url", models.CharField(max_length=255)),
                (
                    "telpunt_naam",
                    models.CharField(help_text="Telpuntnaam", max_length=255),
                ),
                ("tussen", models.CharField(help_text="Tussen", max_length=255)),
                (
                    "richtingen_1",
                    models.CharField(help_text="Richtingen_1", max_length=255),
                ),
                (
                    "richtingen_2",
                    models.CharField(help_text="Richtingen_2", max_length=255),
                ),
                ("jaar", models.IntegerField()),
                ("storing", models.CharField(help_text="storing", max_length=255)),
                (
                    "type_verkeer",
                    models.CharField(help_text="Type_verkeer", max_length=255),
                ),
                ("langzaam_verkeer", models.BooleanField(help_text="Langzaam_verkeer")),
                ("snel_verkeer", models.BooleanField(help_text="Snel_verkeer")),
                (
                    "bijzonderheden",
                    models.CharField(help_text="Bijzonderheden", max_length=255),
                ),
                (
                    "meet_methode",
                    models.CharField(help_text="Meetmethode", max_length=255),
                ),
            ],
            options={
                "verbose_name": "Verkeerstelling",
                "verbose_name_plural": "Verkeerstellingen",
            },
        ),
        migrations.CreateModel(
            name="Verrijking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("link_nr", models.IntegerField(help_text="linknr")),
                ("binnen_amsterdam", models.BooleanField(blank=True, null=True)),
                ("binnen_polygoon_awb", models.BooleanField(blank=True, null=True)),
                ("milieuzone", models.BooleanField(blank=True, null=True)),
                ("zone_zwaar_verkeer_bus", models.BooleanField(blank=True, null=True)),
                (
                    "zone_zwaar_verkeer_non_bus",
                    models.BooleanField(blank=True, null=True),
                ),
                (
                    "zone_zwaar_verkeer_detail",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "tunnelcategorie_gevaarlijke_stoffen",
                    models.CharField(blank=True, max_length=29, null=True),
                ),
                ("tunnelnamen", models.CharField(blank=True, max_length=29, null=True)),
                (
                    "route_gevaarlijke_stoffen",
                    models.CharField(blank=True, max_length=29, null=True),
                ),
                (
                    "beleidsnet_auto",
                    models.CharField(blank=True, max_length=29, null=True),
                ),
                (
                    "beleidsnet_ov",
                    models.CharField(blank=True, max_length=29, null=True),
                ),
                (
                    "beleidsnet_fiets",
                    models.CharField(blank=True, max_length=29, null=True),
                ),
                (
                    "beleidsnet_lopen",
                    models.CharField(blank=True, max_length=29, null=True),
                ),
                (
                    "hoofdroute_taxi",
                    models.CharField(blank=True, max_length=29, null=True),
                ),
                (
                    "touringcar_aanbevolen_routes",
                    models.CharField(blank=True, max_length=29, null=True),
                ),
                (
                    "wettelijke_snelheid_actueel",
                    models.IntegerField(blank=True, null=True),
                ),
                (
                    "wettelijke_snelheid_wens",
                    models.IntegerField(blank=True, null=True),
                ),
                (
                    "wegcategorie_actueel",
                    models.CharField(blank=True, max_length=29, null=True),
                ),
                (
                    "wegcategorie_wens",
                    models.CharField(blank=True, max_length=29, null=True),
                ),
                ("frc", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Verrijking",
                "verbose_name_plural": "Verrijkingen",
            },
        ),
        migrations.CreateModel(
            name="Vma",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("link_nr", models.FloatField()),
                ("name", models.CharField(blank=True, max_length=50, null=True)),
                ("direction", models.FloatField(blank=True, null=True)),
                ("length", models.FloatField(blank=True, null=True)),
                ("anode", models.FloatField(blank=True, null=True)),
                ("bnode", models.FloatField(blank=True, null=True)),
                ("wegtypeab", models.CharField(blank=True, max_length=50, null=True)),
                ("wegtypeba", models.CharField(blank=True, max_length=50, null=True)),
                ("speedab", models.FloatField(blank=True, null=True)),
                ("speedba", models.FloatField(blank=True, null=True)),
                ("wegtype_ab", models.CharField(blank=True, max_length=50, null=True)),
                ("wegtype_ba", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.MultiLineStringField(
                        srid=28992
                    ),
                ),
            ],
            options={
                "verbose_name": "Vma",
                "verbose_name_plural": "Vma",
            },
        ),
    ]
