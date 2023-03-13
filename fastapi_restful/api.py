from typing import Dict, Optional, Type

from fastapi import FastAPI
from starlette.routing import Mount

from .resource import Resource


class RestAPIRouter:
    """
    A class specific version API.
    """

    def __init__(self, path: str):
        self.fastapi = FastAPI()
        self.path = f'/{self._strip_path(path)}'

    def __str__(self) -> str:
        return self.path

    @staticmethod
    def _strip_path(path: Optional[str]) -> str:
        return path.strip("/") if path is not None else ""

    @property
    def urls(self) -> dict:
        """
        Registered urls and HTTP methods.

        Returns
        -------
        Url map
        """
        urls = dict()
        for route in self.fastapi.routes:
            if isinstance(route, Mount):
                continue
            urls.setdefault(route.path, set())
            urls[route.path].update(route.methods)
        return urls

    def add_resource(self, resource: Type[Resource], path: str = None) -> None:
        """
        Initial resource and add resource router to FastAPI.

        Parameters
        ----------
        resource
            Type of Resource
        path
            Resource path

        Returns
        -------
        None
        """
        resource_instance = resource(path)
        self.fastapi.include_router(resource_instance.router)


class RestAPI(RestAPIRouter):
    """Main class for create RESTful-API."""

    def __init__(self, path: Optional[str] = "/api"):
        """
        Init class.

        Parameters
        ----------
        path: Default prefix in url path.
        """
        super().__init__(path)
        self.rest_api_routers: Dict[str, RestAPIRouter] = {}

    def __getitem__(self, item: str) -> Optional[RestAPIRouter]:
        """
        Get instance API by path.

        Parameters
        ----------
        item: path

        Returns
        -------
        Instance of RestAPIRouter or None
        """
        return self.rest_api_routers.get(self.path)

    def init(self, fastapi_app: FastAPI) -> None:
        """
        Include FastAPI app of RestAPI to main FastAPI app.

        Returns
        -------
        None
        """
        fastapi_app.mount(path=self.path, app=self.fastapi)

    def include_rest_api_router(self, rest_api_router: RestAPIRouter) -> None:
        """
        Include API version to main router.

        Parameters
        ----------
        rest_api_router
            Instance of RestAPIRouter with included resources.
        """
        rest_api_path = rest_api_router.path
        if rest_api_path in self.rest_api_routers:
            raise AssertionError(f"This version is exist: {rest_api_path}")
        self.rest_api_routers[rest_api_path] = rest_api_router
        self.fastapi.mount(path=rest_api_path, app=rest_api_router.fastapi)
