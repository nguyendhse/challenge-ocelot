from typing import Any

from ninja_extra import ModelService
from ninja_extra import service_resolver
from ninja_extra.controllers import RouteContext


class BookModelService(ModelService):
    def create(self, schema, **kwargs: Any) -> Any:
        data = schema.dict(by_alias=True)
        data.update(kwargs)
        context: RouteContext = service_resolver(RouteContext)

        created_by = context.request.user
        authors = data.pop('authors')
        book = self.model._default_manager.create(**data, created_by=created_by)
        book.authors.add(*authors)
        return book
