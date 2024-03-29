# Generated by Django 4.0.5 on 2022-06-22 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0009_slugify"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="name",
            field=models.SlugField(
                help_text="Unique slug across all projects", max_length=255, unique=True
            ),
        ),
    ]
