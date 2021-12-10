# Generated by Django 3.1.7 on 2021-03-07 15:09

import django.core.serializers.json
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="JobResult",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("completed", models.DateTimeField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("running", "Running"),
                            ("completed", "Completed"),
                            ("errored", "Errored"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=30,
                    ),
                ),
                (
                    "data",
                    models.JSONField(
                        blank=True,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                        null=True,
                    ),
                ),
                ("job_id", models.UUIDField(unique=True)),
                (
                    "obj_type",
                    models.ForeignKey(
                        help_text="The object type to which this job result applies",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="job_results",
                        to="contenttypes.contenttype",
                        verbose_name="Object type",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created"]},
        )
    ]
