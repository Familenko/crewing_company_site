# Generated by Django 4.2.7 on 2023-11-21 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("crewing", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vessel",
            name="crew",
        ),
        migrations.AddField(
            model_name="crew",
            name="vessel",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="sailors",
                to="crewing.vessel",
            ),
        ),
    ]
