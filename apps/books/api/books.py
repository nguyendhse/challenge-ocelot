from typing import List

from asgiref.sync import sync_to_async
from django.http import Http404, JsonResponse
from ninja import Router, Query, File
from ninja.security import django_auth
from ninja.files import UploadedFile
from ninja_extra.exceptions import ValidationError, ErrorDetail

from apps.books.models import Book, Author, BookCover
from apps.books.schemas import AuthorFilters, BookInSchema, BookSchema, BookFilters, BookCoverInSchema

router = Router(tags=['Books'], )


@router.get("", response=List[BookSchema])  # noqa
async def list_books(request, filters: BookFilters = Query(...)):
    _filter = filters.get_filter_expression()
    qs = await sync_to_async(Book.objects.filter)(_filter)
    return qs


@router.post("", response=BookSchema, auth=django_auth)
async def create_book(request, data: BookInSchema):
    payload_dict = data.dict()
    authors = payload_dict.pop('authors') if 'authors' in payload_dict else []
    book = await Book.objects.acreate(**payload_dict, created_by_id=request.user.id)
    authors = [author async for author in Author.objects.filter(pk__in=authors)]
    book.authors.add(*authors)
    return book


@router.get("{id}", response=BookSchema)
async def retrieve_book(request, id: int):
    book = await Book.objects.filter(pk=id).afirst()
    if not book:
        raise Http404(f"Book id {id} Not found")
    return book


@router.post("{id}/cover/", response=BookSchema)
async def upload_book_cover(request, id: int, file_cover: UploadedFile = File(...)):
    if not file_cover.content_type.startswith('image/'):
        raise ValidationError('Please provide an image (.jpg, .jpeg, .png, .gif, .bmp).')
    book = await Book.objects.filter(pk=id).afirst()
    if not book:
        raise Http404(f"Book id {id} Not found")
    book_cover = await BookCover.objects.acreate(book=book, file=file_cover)
    book.book_covers.add(book_cover)
    return book


@router.put("{id}", response=BookSchema, auth=django_auth)
async def update_book(request, id: int, data: BookInSchema):
    payload_dict = data.dict()

    book = await Book.objects.filter(pk=id).afirst()
    if not book:
        raise Http404(f"Book id {id} Not found")
    authors = payload_dict.pop('authors') if 'authors' in payload_dict else []
    authors = [author async for author in Author.objects.filter(pk__in=authors)]

    for attr, value in payload_dict.items():
        setattr(book, attr, value)
    book.authors.add(*authors)
    return book


@router.delete("{id}", response=BookSchema, auth=django_auth)
async def delete_book(request, id: int):
    book = await Book.objects.filter(pk=id).afirst()
    if not book:
        raise Http404(f"Book id {id} Not found")

    book.delete()
    return JsonResponse({'status': 'success'}, status=200)
