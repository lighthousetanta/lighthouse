from django.db import models
from django.contrib.auth.models import User


class MissingPerson(models.Model):
    pass


class KnownMissingPerson(MissingPerson):
    name = models.CharField(max_length=50)
    contactPerson = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="missingPersons"
    )

    def __str__(self):
        return self.name


class UnKnownMissingPerson(MissingPerson):
    volunter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="InStreetPersons"
    )


class Image(models.Model):
    missingPerson = models.ForeignKey(
        MissingPerson, on_delete=models.CASCADE, related_name="photos"
    )
    imgPath = models.ImageField(upload_to="photos")
    imgEmbedding = models.JSONField()
    takenBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="takenPhotos", default=0
    )

    def __str__(self):
        return f"image for {self.missingPerson} taken by {self.takenBy}"