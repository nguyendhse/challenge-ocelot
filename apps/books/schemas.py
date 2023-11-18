from datetime import datetime

from ninja import Field, FilterSchema, ModelSchema

from apps.books.models import Author, Book, BookCover


class AuthorSchema(ModelSchema):
    class Config:
        model = Author
        model_fields = ["id", "name"]


class AuthorInSchema(ModelSchema):
    class Config:
        model = Author
        model_fields = ["name"]


class AuthorFilters(FilterSchema):
    name: str | None = Field(None, q="name__icontains")


class BookCoverSchema(ModelSchema):
    class Config:
        model = BookCover
        model_fields = ["file"]


class BookCoverInSchema(ModelSchema):
    class Config:
        model = BookCover
        model_fields = ["book", "file"]


class BookSchema(ModelSchema):
    authors: list[AuthorSchema]
    # created_by: Optional[UserRetrieveSchema]
    book_covers: list[BookCoverSchema]

    class Config:
        model = Book
        model_fields = "__all__"


class BookFilters(FilterSchema):
    title: str | None = Field(None, q="title__icontains")
    publish_date: datetime | None = Field(None, q="publish_date__date")


class BookInSchema(ModelSchema):
    class Config:
        model = Book
        model_exclude = ["id", "created_by"]


class BookFilterSchema(FilterSchema):
    title: str | None = None
    author: str | None = None
