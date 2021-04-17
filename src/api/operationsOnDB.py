from .models import KnownMissingPerson, Image
from django.contrib.auth.models import User
from .classifier.classifier import ImageClassifier


class OperationsOnDB:
    def addKnownMissingPerson(name, image):
        # TODO : add form and use Isvalid method
        contactPerson = User.objects.all()[1]
        newMissingPerson = KnownMissingPerson(name=name, contactPerson=contactPerson)
        newMissingPerson.save()
        embedingOfTheImage = ImageClassifier.embed(image)
        imageOfNewMissingPerson = Image(
            missingPerson=newMissingPerson,
            imgPath=image,
            imgEmbedding=embedingOfTheImage,
            takenBy=contactPerson,
        )
        imageOfNewMissingPerson.save()
        return KnownMissingPerson.objects.get(pk=newMissingPerson.pk)

    def getAllKnownMissingPersons():
        # This return list of KnownMissingPersons each record have the following attributes :
        #       - pk    - name           - contactPerson - photos
        #   Each photo have the attributes :
        #       - pk    - missingPerson  - imgPath       - imgEmbedding -takenBy
        return KnownMissingPerson.objects.all()

    def getKnownMissingPerson(pk):
        return KnownMissingPerson.objects.get(pk=pk)

    def deleteKnownMissingPerson(pk):
        missinPerson = KnownMissingPerson.objects.get(pk=pk)
        missinPerson.delete()
        return True

    def searchforKnownMissingPerson(image):
        TargerImageEmbed = ImageClassifier.embed(image)
        # TODO : fix this query to return id of missingperson and his image Embbed
        ImagesEmbeds = KnownMissingPerson.objects.all()
        IdOfMissingPerson = ImageClassifier.find(ImagesEmbeds, TargerImageEmbed)
        return IdOfMissingPerson