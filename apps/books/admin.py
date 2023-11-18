from django.contrib import admin

from apps.books.models import Author, Book

# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "publish_date", "isbn", "price"]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass
