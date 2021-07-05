from singleton import Singleton

from classifier import Model

model1 = Model()

model2 = Model()

model = Model()

print(model is model2 is model1)

embedding = model.get_embedding("image.jpg")
embedding = str(embedding)

print(embedding)
print(len(embedding))
print(type(embedding))
