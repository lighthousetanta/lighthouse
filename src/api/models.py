from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class User(AbstractUser):
    def serialize(self):
        return {
            "id": self.id,
            "user": self.username,
        }


class UserManager(BaseUserManager):
    pass


class KnownMissingPerson(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="knownMissingPersonsImages")
    contactPerson = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="knownMissingPersonsContact",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image.url,
        }


class KnownMissingPersonImages(models.Model):
    missingPerson = models.ForeignKey(
        KnownMissingPerson,
        on_delete=models.CASCADE,
        related_name="knownMissingPersonsImages",
    )
    image = models.ImageField(upload_to="knownMissingPersonsImages")

    def __str__(self):
        return f"image for {self.missingPerson}"

    def serialize(self):
        return {"id": self.id, "url": self.image.url}


class KnownMissingPersonTrackRecord(models.Model):
    missingPerson = models.ForeignKey(
        KnownMissingPerson,
        on_delete=models.CASCADE,
        related_name="foundKnownMissingPersonsImages",
    )
    image = models.ImageField(upload_to="unknownMissingPersonsImages")
    embedding = models.JSONField(blank=True, null=True)
    taken_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="knownMissingPersonsImagesTaker",
        default=0,
    )

    def __str__(self):
        return f"image for {self.missingPerson} taken by {self.taken_by}"


class UnKnownMissingPerson(models.Model):
    pass


class UnknownMissingPersonTrackRecord(models.Model):
    missingPerson = models.ForeignKey(
        UnKnownMissingPerson,
        on_delete=models.CASCADE,
        related_name="foundUnknownMissingPersonsImages",
    )
    image = models.ImageField(upload_to="unknownMissingPersonsImages")
    embedding = models.JSONField(blank=True, null=True)
    taken_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="unknownMissingPersonsImagesTaker",
        default=0,
    )

    def __str__(self):
        return f"image for Unknown Missing person taken by {self.taken_by}"


class Quereies(models.Model):
    image = models.ImageField(upload_to="Queries")
    result = models.JSONField(blank=True, null=True)
