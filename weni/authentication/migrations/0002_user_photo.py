# Generated by Django 2.2.17 on 2020-12-29 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="photo",
            field=models.FileField(null=True, upload_to="", verbose_name="photo user"),
        ),
    ]