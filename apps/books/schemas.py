from datetime import datetime
from typing import Optional, List

from ninja import ModelSchema
from pydantic import BaseModel

from apps.books.models import Book, Author, BookCover
from apps.users.schemas import UserRetrieveSchema

from ninja import FilterSchema, Field


class AuthorSchema(ModelSchema):
    class Config:
        model = Author
        model_fields = ['id', 'name']


class AuthorInSchema(ModelSchema):
    class Config:
        model = Author
        model_fields = ['name']


class AuthorFilters(FilterSchema):
    name: Optional[str] = Field(None, q='name__icontains')


class BookCoverSchema(ModelSchema):
    class Config:
        model = BookCover
        model_fields = ['file']


class BookCoverInSchema(ModelSchema):
    class Config:
        model = BookCover
        model_fields = ['book', 'file']


class BookSchema(ModelSchema):
    authors: List[AuthorSchema]
    created_by: Optional[UserRetrieveSchema]
    book_covers: List[BookCoverSchema]

    class Config:
        model = Book
        model_fields = "__all__"


class BookFilters(FilterSchema):
    title: Optional[str] = Field(None, q='title__icontains')
    publish_date: Optional[datetime] = Field(None, q='publish_date__date')


class BookInSchema(ModelSchema):
    class Config:
        model = Book
        model_exclude = ['id', 'created_by']


class BookFilterSchema(FilterSchema):
    title: Optional[str] = None
    author: Optional[str] = None
