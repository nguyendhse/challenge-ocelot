from asgiref.sync import sync_to_async
from ninja import NinjaAPI, Schema
from ratelimit import RatelimitExceeded

from apps.books.api.authors import router as authors_router
from apps.books.api.books import router as books_router
from apps.users.api.users import router as users_router

api = NinjaAPI(version='1.0', title='Books Store API', csrf=True)
api.add_router("/authors/", authors_router)
api.add_router("/books/", books_router)
api.add_router("/auth/", users_router)


@api.exception_handler(RatelimitExceeded)
def request_exceeded_limited(request, exc):
    return api.create_response(
        request,
        {"message": "You have exceeded the limit. Please retry later"},
        status=429,
    )
