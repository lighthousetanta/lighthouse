from django.http import JsonResponse

from .base import BaseViewSet
from ..classifier.classifier import Model
from ..classifier.index import SearchIndex
from ..models import KnownMissingPerson, Quereies
import threading
import json


class FindMissingViewSet(BaseViewSet):
    def __init__(self, request):
        super().__init__(request)
        self.request = request
        self.verbs = {"POST": self.post}

    def post(self):
        target_image = self.request.FILES["image"]
        query = Quereies(image=target_image)
        query.save()
        threading.Thread(target=self.async_search, args=[query]).start()
        response = {"id": query.id, "time": "10"}
        return JsonResponse(response)

    def async_search(self, query):
        embedding = self.get_embedding(query.image)
        query_res = self.search(embedding)
        self.update_queries_table(query_res, query.id)
        print("background job done")

    def get_embedding(self, image):
        model = Model()
        embedding = model.get_embedding(image)
        print("embeeding done")
        return embedding

    def search(self, embedded_image):
        query_res = {}
        index = SearchIndex()
        result = index.search(embedded_image, 3)
        for i in result["hits"]["hits"]:
            score = i["_score"]
            id = i["_id"]
            query_res[id] = score
        print("search done")
        print(query_res)
        return query_res

    def update_queries_table(self, query_res, query_id):
        query = Quereies.objects.get(id=query_id)
        query.result = query_res
        query.save()
        print("database done")


class ResultViewSet(BaseViewSet):
    def __init__(self, request):
        super().__init__(request)
        self.request = request
        self.verbs = {"GET": self.get}

    def get(self):
        response = []
        body_unicode = self.request.body.decode("utf-8")
        body = json.loads(body_unicode)
        query_id = body["id"]
        query = Quereies.objects.get(id=query_id)
        if not query.result:
            return JsonResponse({"message": "try again"})
        for id, score in query.result.items():
            person = KnownMissingPerson.objects.get(id=int(id))
            response.append({"person": person.serialize(), "score": score})
        return JsonResponse(response, safe=False)
