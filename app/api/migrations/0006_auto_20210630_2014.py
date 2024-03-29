# Generated by Django 3.2 on 2021-06-30 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0005_knownmissingperson_embedding"),
    ]

    operations = [
        migrations.CreateModel(
            name="KnownMissingPersonTrackRecord",
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
                ("image", models.ImageField(upload_to="unknownMissingPersonsImages")),
                ("embedding", models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="UnknownMissingPersonTrackRecord",
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
                ("image", models.ImageField(upload_to="unknownMissingPersonsImages")),
                ("embedding", models.JSONField(blank=True, null=True)),
                (
                    "missingPerson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="foundUnknownMissingPersonsImages",
                        to="api.unknownmissingperson",
                    ),
                ),
                (
                    "taken_by",
                    models.ForeignKey(
                        default=0,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="unknownMissingPersonsImagesTaker",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="userseeunknownmissingperson",
            name="missingPerson",
        ),
        migrations.RemoveField(
            model_name="userseeunknownmissingperson",
            name="takenBy",
        ),
        migrations.RenameField(
            model_name="knownmissingpersonimages",
            old_name="imgPath",
            new_name="image",
        ),
        migrations.RemoveField(
            model_name="knownmissingperson",
            name="embedding",
        ),
        migrations.RemoveField(
            model_name="knownmissingpersonimages",
            name="embedding",
        ),
        migrations.DeleteModel(
            name="UserSeeKnownMissingPerson",
        ),
        migrations.DeleteModel(
            name="UserSeeUnknownMissingPerson",
        ),
        migrations.AddField(
            model_name="knownmissingpersontrackrecord",
            name="missingPerson",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="foundKnownMissingPersonsImages",
                to="api.knownmissingperson",
            ),
        ),
        migrations.AddField(
            model_name="knownmissingpersontrackrecord",
            name="taken_by",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="knownMissingPersonsImagesTaker",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
