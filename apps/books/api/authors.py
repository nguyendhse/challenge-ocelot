from asgiref.sync import sync_to_async
from django.http import Http404, JsonResponse
from ninja import Query, Router
from ninja.security import django_auth

from apps.books.models import Author
from apps.books.schemas import AuthorFilters, AuthorInSchema, AuthorSchema

router = Router(
    tags=["Authors"],
)


@router.get("", response=list[AuthorSchema])
async def list_authors(request, filters: AuthorFilters = Query(...)):
    _filter = filters.get_filter_expression()
    qs = await sync_to_async(Author.objects.filter)(_filter)
    return qs


@router.post("", response=AuthorSchema, auth=django_auth)
async def create_author(request, data: AuthorInSchema):
    author = await Author.objects.acreate(**data.dict())
    return author


@router.get("{id}", response=AuthorSchema)
async def retrieve_author(request, id: int):
    author = await Author.objects.filter(pk=id).afirst()
    if not author:
        raise Http404(f"Author id {id} Not found")
    return author


@router.put("{id}", response=AuthorSchema, auth=django_auth)
async def update_author(request, id: int, data: AuthorInSchema):
    author = await Author.objects.filter(pk=id).afirst()
    if not author:
        raise Http404(f"Author id {id} Not found")

    for attr, value in data.dict().items():
        setattr(author, attr, value)
    await author.asave()
    return author


@router.delete("{id}", response=AuthorSchema, auth=django_auth)
async def delete_author(request, id: int):
    author = await Author.objects.filter(pk=id).afirst()
    if not author:
        raise Http404(f"Author id {id} Not found")

    author.delete()
    return JsonResponse({"status": "success"}, status=200)
