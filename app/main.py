import uvicorn
from fastapi import FastAPI

from app.core import get_settings, db
from app.apis import auth_router

settings = get_settings()


def init_app():
    db.init()

    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION
    )

    @app.on_event("startup")
    async def startup():
        await db.create_all()

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    app.include_router(auth_router)

    return app


root = init_app()


def start():
    """Launched with 'poetry run start' at root level """
    uvicorn.run(app="app.main:root", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
