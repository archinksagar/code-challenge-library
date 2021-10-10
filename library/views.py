from django.http import response
from rest_framework.response import Response
from rest_framework import status
from library.models import Library
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import Book, Library, Category, Language, Transaction, User
from .serializers import LibraryBooksSerializer, LibrarySerializer, UserBooksSerializer, UserSerializer, CategorySerializer, LanguageSerializer, BookSerializer, TransactionSerializer
from rest_framework.decorators import action


class LibraryViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LibrarySerializer
    queryset = Library.objects.all()
    lookup_field = 'id'

    # To retrieve all the books of a given library
    @action(detail=True, methods=["GET"])
    def books(self, request, id = None):

        library = self.get_object()
        books = library.library_books.all().order_by("title")
        borrowed = self.request.query_params.get('borrowed')
        if borrowed is not None:
            books = books.filter(is_borrowed=borrowed)
        serializer = LibraryBooksSerializer(books, many = True)
        
        return Response(serializer.data)

class CategoryViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class LanguageViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()

class BookViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BookSerializer
    queryset = Book.objects.all()

class UserViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    # retrieving all the books of a given user
    @action(detail=True, methods=["GET"])
    def books(self, request, id = None):

        # ordering the resultset by due_date ascending
        transactions = Transaction.objects.filter(user = self.get_object()).order_by('due_date')

        # filtering the resultset by due_date passed
        due_date = self.request.query_params.get('due_date')

        if due_date is not None:
            transactions = transactions.filter(due_date=due_date)
        serializer = UserBooksSerializer(transactions, many = True)

        return Response(serializer.data)

class TransactionViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        queryset = Transaction.objects.all().order_by('due_date')
        
        try:
            # reading filters from query params
            user = self.request.query_params.get('user')
            book = self.request.query_params.get('book')
            due_date = self.request.query_params.get('due_date')
            library = self.request.query_params.get('library')

            # validating query params
            if user is not None:
                queryset = queryset.filter(user=user)
            if book is not None:
                queryset = queryset.filter(book=book)
            if due_date is not None:
                queryset = queryset.filter(due_date=due_date)
            if library is not None:
                queryset = queryset.filter(library_borrowed=library)
            return queryset
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        transaction_data = request.data

        try:
            book = Book.objects.get(pk=transaction_data['book'])
        except:
            return response.JsonResponse({"error": "Book not found."}, status=404)

        # check if the book is available to borrow and not already borrowed
        # before letting someone borrow the book
        if book.is_active and not book.is_borrowed:
            user = User.objects.get(pk=transaction_data['user'])
            borrowed_from = Library.objects.get(name = book.library)

            # creating a new transaction
            new_transaction = Transaction.objects.create(
                book = book,
                user = user,
                library_borrowed = borrowed_from)

            new_transaction.save()
            
            # updating the borrowed status of the book
            # to prevent someone else from borrowing it
            book.is_borrowed = True
            book.save()

            serializer = TransactionSerializer(new_transaction)
            return Response(serializer.data)
        else:
            return response.JsonResponse({"message": "Book is alreay Borrowed."}, status=404)

    def update(self, request, *args, **kwargs):
        # reading request body json
        transaction_data = request.data
        
        try:
            try:
                # retrieving the library instance for the library the user is retuning the book to 
                library = Library.objects.get(pk=transaction_data['library_returned'])
                # check if the book instance exists in the database
                # if book is none then throw error
                book = Book.objects.get(pk=transaction_data['book'])
            except:
                return response.JsonResponse({"error": "Book or Library not found."}, status=404)

            # updating book returned date and the library it is returned to
            transaction = Transaction.objects.get(pk=transaction_data['id'])
            transaction.return_date = transaction_data['return_date']
            transaction.library_returned = library
            transaction.save()
            
            # updating the borrowed status of the book and the current library of the book
            book.is_borrowed = False
            book.library = library
            book.save()

            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        