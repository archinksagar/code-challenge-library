from django.db.models import fields
from rest_framework import serializers
from .models import Library, Transaction, User, Category, Language, Book


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User  
        fields = ('id','username','first_name','last_name','email')

class LibrarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Library
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'

class LibraryBooksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id','title','is_borrowed')

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'

class UserBooksSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source='book.title')
    class Meta:
        model = Transaction
        fields = ('book','due_date')
