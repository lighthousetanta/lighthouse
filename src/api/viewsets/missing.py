from .. import models
from django.http import JsonResponse
from django.db import IntegrityError
from .base import BaseViewSet
from ..utils import get_user
from ..classifier.index import SearchIndex
from ..classifier.classifier import Model
import threading


class MissingViewSet(BaseViewSet):
    def __init__(self, request):
        super().__init__(request)
        self.verbs = {"GET": self.get, "POST": self.post}

    def post(self):
        files = self.request.FILES
        data = self.request.POST
        name = data["name"]
        image = files["image"]
        try:
            user = get_user(self.request)
            person = models.KnownMissingPerson(
                contactPerson=user, name=name, image=image
            )
            person.save()
            threading.Thread(target=self.save_embedding, args=[person]).start()
            return JsonResponse(person.serialize(), status=201)
        except IntegrityError:
            return JsonResponse({"message": "Database integrity error"}, status=500)

    def save_embedding(self, person):
        embedding = Model().get_embedding(person.image)
        person.embedding = str(embedding)
        person.save()
        SearchIndex().push(embedding, person.id)
        print("posted")

    @staticmethod
    def get():
        people = models.KnownMissingPerson.objects.all()
        response = [person.serialize() for person in people]
        return JsonResponse(response, safe=False)


class MissingIdViewSet(BaseViewSet):
    def __init__(self, request, pk):
        super().__init__(request)
        self.pk = pk
        self.verbs = {"GET": self.get, "DELETE": self.delete, "PATCH": self.patch}

    def get(self):
        try:
            person = models.KnownMissingPerson.objects.get(id=self.pk)
            person = person.serialize()
            return JsonResponse(person, safe=False)
        except IntegrityError:
            return JsonResponse({"message": "Database integrity error"}, status=500)

    def delete(self):
        person = models.KnownMissingPerson.objects.get(id=self.pk)
        person.delete()
        SearchIndex().delete(self.pk)
        return JsonResponse({"message": "deleted"}, status=204)

    def patch(self):
        person = models.KnownMissingPerson.objects.get(id=self.pk)
        data = dict(self.request.PATCH)
        data = {**data, **self.request.FILES}
        for attribute, value in data.items():
            if isinstance(value, list):
                value = value[0]
            setattr(person, attribute, value)
        person.save()
        return JsonResponse(person.serialize(), status=202)
