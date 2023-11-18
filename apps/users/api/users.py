from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from ninja import Router
from ninja.errors import ValidationError

from apps.users.schemas import RegistrationSchema, UserRetrieveSchema

router = Router(
    tags=["Users"],
)
User = get_user_model()


@router.post("/register", response=UserRetrieveSchema)
async def register(request, payload: RegistrationSchema):
    if payload.password1 != payload.password2:
        raise ValidationError(["Passwords do not match"])
    if User.objects.filter(username=payload.username).exists():
        raise ValidationError("Username already taken")

    user = await sync_to_async(User.objects.create_user)(
        username=payload.username, password=payload.password1, email=payload.email, name=payload.name
    )

    return user
