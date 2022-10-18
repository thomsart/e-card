from django.contrib import admin
from account.models import Phone

class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Phone, AuthorAdmin)