from django.db import models


class BookManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_active=True)
