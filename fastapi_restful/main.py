from typing import Type

from fastapi import FastAPI

from .resource import Resource


class Api:
    """A class for create RESTfull-API."""

    fastapi: FastAPI = None

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

    def add_resource(self, resource: Type[Resource], path: str = None) -> None:
        """
        Initial resource and add resource router to FastAPI.

        Parameters
        ----------
        resource: Type of Resource
        path: Resource path

        Returns
        -------
        None
        """
        res = resource(path)
        self.fastapi.include_router(res.router)
