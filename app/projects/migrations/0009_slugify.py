# Generated by Django 4.0.5 on 2022-06-22 20:53

from django.db import migrations
from django.utils.text import slugify


def forward(apps, schema_editor):
    Project = apps.get_model("projects", "Project")
    for project in Project.objects.all():
        project.name = slugify(project.name)
        project.save()


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0008_alter_project_name_alter_project_packages_token"),
    ]

    operations = [
        migrations.RunPython(forward, reverse_code=migrations.RunPython.noop),
    ]
