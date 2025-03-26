from logging import Logger
from logging import getLogger

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRoute

from app.apis import route

from .core.config import settings
from .lifespan import lifespan

logger: Logger = getLogger(__name__)


def custom_generate_unique_id(route: APIRoute) -> str:
    if route.tags:
        return f"{route.tags[0]}-{route.name}"
    return route.name


app: FastAPI = FastAPI(
    title=settings.project.name,
    lifespan=lifespan,
    generate_unique_id_function=custom_generate_unique_id,
    default_response_class=ORJSONResponse,
    swagger_ui_parameters={
        "persistAuthorization": True,
        "filter": True,
        "displayRequestDuration": True,
        "defaultModelRendering": "model",
    },
)


app.include_router(route, prefix="/v1")
