from drf_yasg import openapi
from rest_framework.serializers import Serializer
from functools import wraps
from django.http import JsonResponse


def get_response_examples(
    example: dict = {},
    description: str = '',
    schema: Serializer | Serializer | None = None,
):
    if schema is None:
        return openapi.Response(
            description=description,
            examples={"application/json": {'error': False} | example},
        )

    return openapi.Response(
        description=description,
        schema=schema
    )

def site_authenticated(view_func):

    @wraps(view_func)
    async def _wrapped_view(request, *args, **kwargs):
        site_access = request.COOKIES.get("access_token")
        site_refresh = request.COOKIES.get("refresh_token")


        if not site_access or not site_refresh:
            return JsonResponse({"detail": "Unauthorized"}, status=401)

        if not site_access:
            return JsonResponse({"detail": "Need create Acces"}, status=401)


        return await view_func(request, *args, **kwargs)

    return _wrapped_view