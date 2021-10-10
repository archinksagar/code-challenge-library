from django.contrib import admin
from .models import Book, Transaction, User, Library, Category, Language

admin.site.register(User)
admin.site.register(Library)
admin.site.register(Category)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(Transaction)