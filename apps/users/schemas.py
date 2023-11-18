from django.contrib.auth import get_user_model
from ninja import ModelSchema, Schema


class UserRetrieveSchema(ModelSchema):
    class Config:
        model = get_user_model()
        model_fields = ("email", "name", "username", "id", "is_active")


class RegistrationSchema(Schema):
    username: str
    password1: str
    password2: str
    email: str | None
    name: str | None
