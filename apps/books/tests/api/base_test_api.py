from django.contrib.auth import get_user_model
from django.test import TestCase


class BaseApiTestCase(TestCase):
    @classmethod
    def init_users(cls):
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="12345678ABC",
        )
        cls.user_id = cls.user.id

    @classmethod
    def setUpTestData(cls):
        cls.init_users()

    def setUp(self) -> None:
        self.user = get_user_model().objects.get(pk=self.user_id)
