from django.contrib import admin
from .models import MissingPerson, Image, UnKnownMissingPerson, KnownMissingPerson

admin.site.register(MissingPerson)
admin.site.register(UnKnownMissingPerson)
admin.site.register(KnownMissingPerson)
admin.site.register(Image)