from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import PROTECT
from datetime import datetime, timedelta

class User(AbstractUser):
    pass

class Library(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Language(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    is_borrowed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=PROTECT,related_name="category_books")
    language = models.ForeignKey(Language,on_delete=PROTECT,related_name="lang_books")
    library = models.ForeignKey("Library",related_name='library_books',on_delete=PROTECT)

    def __str__(self):
        return f"{self.title}"

def fourteen_days_from_today():
    return (datetime.today() + timedelta(14)).strftime("%Y-%m-%d")

class Transaction(models.Model):
    book = models.ForeignKey("Book",related_name='transactions',on_delete=PROTECT)
    user = models.ForeignKey("User", related_name='borrowed_book',on_delete=PROTECT)
    borrowed_date = models.DateField(auto_now=True)
    due_date = models.DateField(default=fourteen_days_from_today())
    return_date = models.DateField(null=True,blank=True)
    library_borrowed = models.ForeignKey("Library",related_name='transactions_borrowed',on_delete=PROTECT)
    library_returned = models.ForeignKey("Library",related_name='transactions_returned',on_delete=PROTECT,null=True,blank=True)


    def __str__(self):
         return f"{self.book} {self.user} {self.due_date}"