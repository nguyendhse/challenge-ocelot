from typing import Any
from unittest.mock import AsyncMock

import django
from django.http import QueryDict
from django.urls import reverse_lazy
from mixer.backend.django import mixer
from ninja.testing import TestAsyncClient
from ninja.testing.client import build_absolute_uri

from apps.api_router import api
from apps.books.tests.api.base_test_api import BaseApiTestCase


class TestClientCustom(TestAsyncClient):
    def request(self, method, path, data=dict, json=None, **request_params: Any):
        headers = {
            "REMOTE_ADDR": "testclient",
            "X_FORWARDED_FOR": "testclient",
        }
        request_params["headers"] = headers
        return super().request(method, path, data, json, **request_params)

    def _build_request(self, method: str, path: str, data: dict, request_params: Any) -> AsyncMock:
        request = AsyncMock()
        request.method = method
        request.path = path
        request.body = ""
        request.COOKIES = {}
        request._dont_enforce_csrf_checks = True
        request.is_secure.return_value = False
        request.build_absolute_uri = build_absolute_uri

        if "user" not in request_params:
            request.user.is_authenticated = False

        request.META = request_params.pop("META", {})
        request.FILES = request_params.pop("FILES", {})

        request.META.update({f"HTTP_{k.replace('-', '_')}": v for k, v in request_params.pop("headers", {}).items()})
        if django.VERSION[:2] > (2, 1):
            from ninja.compatibility.request import HttpHeaders

            request.headers = HttpHeaders(request.META)  # type: ignore

        if isinstance(data, QueryDict):
            request.POST = data
        else:
            request.POST = QueryDict(mutable=True)

            if isinstance(data, (str, bytes)):
                request_params["body"] = data
            elif data:
                for k, v in data.items():
                    request.POST[k] = v

        if "?" in path:
            request.GET = QueryDict(path.split("?")[1])
        else:
            request.GET = QueryDict()

        for k, v in request_params.items():
            setattr(request, k, v)
        return request


# @override_settings(RATELIMIT_ENABLE=False)
class TestBooksAPI(BaseApiTestCase):
    def setUp(self):
        super().setUp()
        self.books = mixer.cycle(10).blend("books.Book", created_by=self.user, is_active=True)

    async def test_api_list_books(self):
        url = reverse_lazy("api-1.0:list_books")
        response = await self.async_client.get(url)
        self.assertEqual(response.status_code, 200)
        books_list = response.json()
        self.assertEqual(len(books_list), len(self.books))

    async def test_api_create_book_not_authenticated(self):
        url = reverse_lazy("api-1.0:create_book")
        response = await self.async_client.post(url)
        self.assertEqual(response.status_code, 401)

    async def test_api_create_book_success(self):
        data = {
            "title": "Book 1",
            "publish_date": "2023-11-18",
            "isbn": "012345",
            "price": 10,
            "is_active": True,
            "authors": [],
        }
        client = TestClientCustom(api)
        with self.settings(RATELIMIT_ENABLE=False):
            response = await client.post("/books/", json=data, user=self.user)
            self.assertEqual(response.status_code, 200)
            book = response.json()
            self.assertEqual(book.get("title"), data.get("title"))

    async def test_api_retrieve_book_notfound(self):
        url = reverse_lazy("api-1.0:retrieve_book", args=[404])
        response = await self.async_client.get(url)
        self.assertEqual(response.status_code, 404)

    async def test_api_retrieve_book_success(self):
        url = reverse_lazy("api-1.0:retrieve_book", args=[self.books[0].id])
        response = await self.async_client.get(url)
        self.assertEqual(response.status_code, 200)
        book = response.json()
        self.assertEqual(book.get("title"), self.books[0].title)
