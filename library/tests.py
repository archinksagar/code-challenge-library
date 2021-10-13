from library.models import Book, Category, Language, Library, Transaction, User
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetup(APITestCase):

    def setUp(self):
        self.library_data = [{"name":"Brambleton Library","location":"Ashburn, VA"},{"name":"Leesburg Library","location":"Leesburg, VA"}]
        self.books_data = [{"title":"Diary of a Wimpy Kid","author":"Jeff kinney","isbn":"1234567891234","is_borrowed":False,"is_active":True,"category":3,"language":3,"library":2},{"title":"Frozen","author":"akansha","isbn":"1234567891235","is_borrowed":False,"is_active":True,"category":4,"language":2,"library":2},{"title":"Rapunzel","author":"ameya","isbn":"1234567891236","is_borrowed":False,"is_active":True,"category":4,"language":2,"library":2},{"title":"Elephant","author":"michael","isbn":"23456787","is_borrowed":False,"is_active":True,"category":3,"language":2,"library":1},{"title":"Fancy nancy","author":"nancy","isbn":"23443222","is_borrowed":False,"is_active":True,"category":2,"language":1,"library":2},{"title":"nancy 3","author":"sfs","isbn":"34332322","is_borrowed":False,"is_active":True,"category":1,"language":2,"library":1},{"title":"Nancy 4","author":"sfs","isbn":"34332322","is_borrowed":False,"is_active":True,"category":1,"language":2,"library":2}]
        self.transactions_data = [{"book":1,"user":3},{"book":2,"user":1},{"book":3,"user":2},{"book":4,"user":2},{"book":5,"user":1},{"book":6,"user":3}]
        self.category_data = [{"name":"Adult"},{"name":"Kids"},{"name":"Juvenile"},{"name":"Teen"}]
        self.language_data = [{"name":"French"},{"name":"German"},{"name":"English"},{"name":"Spanish"},{"id":5,"name":"Hindi"},{"name":"Telugu"},{"name":"Sanskrit"}]
        self.user_data = [{"username":"admin","first_name":"","last_name":"","email":"admin@somemail.com"},{"username":"archin","first_name":"archana","last_name":"sagar","email":"sagar@somemail.com"},{"username":"tom","first_name":"tom","last_name":"brady","email":"brady@somemail.com"},{"username":"harry","first_name":"harry","last_name":"potter","email":"potter@somemail.com"},{"username":"brapdad81","first_name":"Kal","last_name":"Mah","email":"kalmah@mailinator.com"}]
        #creating library
        for library in self.library_data:
            self.library = Library.objects.create(
                        name = library['name'],
                        location = library['location'])

        #creating category
        for category in self.category_data:
            self.category = Category.objects.create(
                        name = category['name'])

        #creating language
        for language in self.language_data:
            self.language = Language.objects.create(
                        name = language['name'])

        #creating users
        for user in self.user_data:
            self.user = User.objects.create(
                        username = user['username'],
                        first_name = user['first_name'],
                        last_name = user['last_name'],
                        email = user['email'])

        #creating books
        for book in self.books_data:
            self.books = Book.objects.create(
                        title = book['title'],
                        author = book['author'],
                        isbn = book['isbn'],
                        is_borrowed = book['is_borrowed'],
                        is_active = book['is_active'],
                        category = Category.objects.get(pk=book['category']),
                        language = Language.objects.get(pk=book['language']),
                        library = Library.objects.get(pk=book['library']))

        #creating transactions
        for transaction in self.transactions_data:
            book = Book.objects.get(pk=transaction['book'])
            self.transactions = Transaction.objects.create(
                        book = book,
                        user = User.objects.get(pk=transaction['user']),
                        library_borrowed = Library.objects.get(name=book.library))
        return super().setUp()

    # Getting user List
    def test_user_list(self):
        response = self.client.get(reverse("User_view-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Retrieving user 
    def test_user_retrieve(self):
        response = self.client.get(reverse("User_view-detail", kwargs = {"id":1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # creating library
    def test_create_library(self):
        d = {
                "name": "Rust Library",
                "location": "Rust, VA"
            }
        response = self.client.post("/library/", d)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # lists all the libraries
    def test_library_list(self):
        response = self.client.get(reverse("Library_view-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # retrieve library
    def test_library_retrieve(self):
        response = self.client.get(reverse("Library_view-detail", kwargs = {"id":1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # update library 
    def test_library_update(self):
        response = self.client.put(reverse("Library_view-detail", kwargs={"id":1}),
                                {
                                    "id": 1,
                                    "name": "Brambleton Library",
                                    "location": "Brambleton, VA"
                                },)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # create a book
    def test_create_book(self):
        d = {
                "title": "Diary of a Wimpy Kid",
                "author": "Jeff kinney",
                "isbn": "1234567891234",
                "is_borrowed": False,
                "is_active": True,
                "category": 3,
                "language": 3,
                "library": 2
            }
        response = self.client.post("/books/", d)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # list the books
    def test_book_list(self):
        response = self.client.get(reverse("book_view-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # retrieve book
    def test_book_retrieve(self):
        response = self.client.get(reverse("book_view-detail", kwargs = {"pk":1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # update book
    def test_book_update(self):
        response = self.client.put(reverse("book_view-detail", kwargs={"pk":1}),
                                {
                                    "id": 1,
                                    "title": "Diary of a Wimpy Kid",
                                    "author": "Jeff kinney",
                                    "isbn": "1234567891234",
                                    "is_borrowed": False,
                                    "is_active": True,
                                    "category": 4,
                                    "language": 3,
                                    "library": 2
                                },)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # create transaction and testing status of book's (is_borrowed) is set to True
    def test_create_transaction(self):
        d = {
                "book": 6,
                "user": 3
            }
        response = self.client.post("/transactions/", d)
        book = Book.objects.get(pk=6)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(book.is_borrowed, True)

    # list all transactions
    def test_transaction_list(self):
        response = self.client.get(reverse("transaction_view-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # retrieve transaction
    def test_transaction_retrieve(self):
        response = self.client.get(reverse("transaction_view-detail", kwargs = {"pk":1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # update a transaction with return date and returned library
    # testing status of the book(is_borrowed) is set to false
    # testing library of the book (library) is changed to the returned library
    def test_transaction_update(self):
        response = self.client.put(reverse("transaction_view-detail", kwargs={"pk":1}),
                                {
                                    "id": 1,
                                    "return_date": "2021-10-11",
                                    "book": 1,
                                    "library_returned": 1
                                })
        book = Book.objects.get(pk=1)
        library = Library.objects.get(pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(book.is_borrowed, False)
        self.assertEqual(book.library, library)

    # Get all the rented books of the user
    def test_user_books_list(self):
        response = self.client.get("/users/1/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)   

    # List of books in a library and their status
    def test_library_books_list(self):
        response = self.client.get("/library/1/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK) 


        


