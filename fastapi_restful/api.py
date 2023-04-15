from typing import Dict, Optional, Type

from fastapi import FastAPI
from starlette.routing import Mount

from .resource import Resource


class RestAPI:
    """
    A class specific version API.
    """

    def __init__(self, path: str):
        self.app = FastAPI()
        self.path = f"/{self._strip_path(path)}"

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
        for route in self.app.routes:
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
        self.app.include_router(resource_instance.router)


class RESTExtension(RestAPI):
    """Main class for create RESTful-API."""

    def __init__(self, path: Optional[str] = "/api"):
        """
        Init class.

        Parameters
        ----------
        path: Default prefix in url path
        """
        super().__init__(path)
        self.rest_api_map: Dict[str, RestAPI] = {}

    def __getitem__(self, item: str) -> Optional[RestAPI]:
        """
        Get instance API by path.

        Parameters
        ----------
        item: path

        Returns
        -------
        Instance of RESTExtension or None
        """
        return self.rest_api_map.get(self.path)

    def mount_to_app(self, fastapi_app: FastAPI) -> None:
        """
        Include FastAPI app of RESTExtension to main FastAPI app.

        Returns
        -------
        None
        """
        fastapi_app.mount(path=self.path, app=self.app)

    def add_api(self, api: RestAPI) -> None:
        """
        Include API version to main router.

        Parameters
        ----------
        api
            Instance of RESTExtension with included resources.
        """
        rest_api_path = api.path
        if rest_api_path in self.rest_api_map:
            raise AssertionError(f"RestAPI with this prefix is exist: {rest_api_path}")
        self.rest_api_map[rest_api_path] = api
        self.app.mount(path=rest_api_path, app=api.app)
