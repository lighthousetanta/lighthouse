from deepface.basemodels import Facenet
from deepface.commons import functions
from .singleton import Singleton
import platform
import urllib


class Model(metaclass=Singleton):
    def __init__(self):
        self.target_size = (160, 160)
        self.embedding_size = 128
        self.model = Facenet.loadModel()

    def get_embedding(self, image):
        """Takes an image with only the desired face"""
        image = self.get_image_from_url(image.url)
        preprocessed_face = functions.preprocess_face(
            image, target_size=self.target_size, detector_backend="mtcnn"
        )
        return self.model.predict(preprocessed_face)[0]

    def get_image_from_url(self, url):
        urllib.request.urlretrieve(
            url,
            "image.jpg",
        )
        return "image.jpg"
