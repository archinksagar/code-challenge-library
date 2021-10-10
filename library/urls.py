
from django.urls import path
from .views import LibraryViewset, UserViewset, CategoryViewset, LanguageViewset, BookViewset, TransactionViewset
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewset, 'User_view')
router.register(r'library', LibraryViewset, 'Library_view')
router.register(r'category', CategoryViewset, 'category_view')
router.register(r'languages', LanguageViewset, 'language_view')
router.register(r'books', BookViewset, 'book_view')
router.register(r'transactions', TransactionViewset, 'transaction_view')

urlpatterns = [
    path('', include(router.urls)),
]