from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


def book_cover_directory_path(instance, filename):
    return f"book_covers/{instance.book.id}/{filename}"


class Author(models.Model):
    name = models.CharField(_("Name of Author"), blank=True, max_length=255)

    def __str__(self):
        return self.name.capitalize()


class Book(models.Model):
    title = models.CharField(_("Book title"), max_length=255)
    authors = models.ManyToManyField(Author, related_name="books", max_length=255)
    publish_date = models.DateField(_("Publish date"))
    isbn = models.CharField(max_length=13)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(get_user_model(), verbose_name=_("Created by User"), on_delete=models.CASCADE)
    is_active = models.BooleanField(_("Is active"), default=True)

    # objects = BookManager()


class BookCover(models.Model):
    # mimetype_validator = MimetypeValidator(['image/png', 'image/jpg', 'image/jpeg', 'image/gif', 'image/bmp'])

    book = models.ForeignKey("Book", related_name="book_covers", on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=book_cover_directory_path,
    )
