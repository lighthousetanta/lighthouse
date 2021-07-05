from elasticsearch import Elasticsearch, RequestError
from .singleton import Singleton


class SearchIndex(metaclass=Singleton):
    def __init__(self):

        self.es = Elasticsearch([{"host": "localhost", "port": "9200"}])

        mapping = {
            "mappings": {
                "properties": {
                    "title_vector": {"type": "dense_vector", "dims": 128},
                    "title_name": {"type": "keyword"},
                }
            }
        }

        try:
            self.es.indices.create(index="final_face_recognition", body=mapping)

        except RequestError:
            print("Index already exists!!")

    def push(self, emb, index, image_name=None):
        doc = {"title_vector": emb, "title_name": image_name}
        self.es.create("final_face_recognition", id=index, body=doc)

    def delete(self, index):
        self.es.delete(index="final_face_recognition", id=index)

    def search(self, emb, size):
        """
        size : # nearest neighbours
        """
        query = {
            "size": size,  # foe ex 5 nearest neighbours
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.queryVector, 'title_vector')+1",
                        # "source": "1 / (1 + l2norm(params.queryVector, 'title_vector'))", #euclidean distance
                        "params": {"queryVector": list(emb)},
                    },
                }
            },
        }

        res = self.es.search(index="final_face_recognition", body=query)
        return res
