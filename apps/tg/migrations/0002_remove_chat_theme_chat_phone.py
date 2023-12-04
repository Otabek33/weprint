# Generated by Django 4.2.7 on 2023-12-01 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tg", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chat",
            name="theme",
        ),
        migrations.AddField(
            model_name="chat",
            name="phone",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="tg.theme",
            ),
        ),
    ]
