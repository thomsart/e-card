from django.contrib import admin
from card.models import Card

class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Card, AuthorAdmin)