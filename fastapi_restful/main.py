from typing import Type

from fastapi import FastAPI

from .resource import Resource


class Api:

    fastapi: FastAPI

    def __init__(self, fastapi_app: FastAPI = None):
        if fastapi_app is not None:
            self.init_fastapi(fastapi_app)

    def init_fastapi(self, fastapi_app: FastAPI) -> None:
        """
        Will connect the FastAPI application to this Api instance.

        Parameters
        ----------
        fastapi_app: FastAPI application instance.

        Returns
        -------
        None
        """
        self.fastapi = fastapi_app

    def add_resource(self, resource: Type[Resource], url: str = None) -> None:
        res = resource(url)
        self.fastapi.include_router(res.router)
