from fastapi import APIRouter

from app.apis.routes import crawlers

route = APIRouter()

route.include_router(crawlers.router, prefix="/crawlers")
