from django.contrib import admin

from apps.books.models import Author, Book


# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'publish_date', 'isbn', 'price']


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
