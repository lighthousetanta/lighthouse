from rest_framework import serializers
from .models import KnownMissingPerson


class KnownMissingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnownMissingPerson
        fields = "__all__"


# class ContactPersonSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ContactPerson
#         fields ='__all__'
