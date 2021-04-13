# Generated by Django 2.2.19 on 2021-03-31 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0008_service_maintenance"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="project",
            unique_together={("flow_organization",)},
        ),
        migrations.RemoveField(
            model_name="project",
            name="flow_organization_id",
        ),
    ]