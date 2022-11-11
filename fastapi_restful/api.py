from typing import Dict, Optional, Type, Union

from fastapi import APIRouter, FastAPI

from .resource import Resource


class APIMixin:
    router: APIRouter

    @staticmethod
    def _strip_prefix(prefix: Optional[str]) -> str:
        return prefix.strip("/") if prefix is not None else ""

    @property
    def urls(self) -> dict:
        """
        Registered urls and HTTP methods.

        Returns
        -------
        Url map
        """
        urls = dict()
        for route in self.router.routes:
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
        self.router.include_router(resource_instance.router)


class APIVersion(APIMixin):
    """
    A class specific version API.
    """

    def __init__(self, version_prefix: str):
        prefix = self._strip_prefix(version_prefix)
        self.router = APIRouter(prefix=f"/{prefix}")

    def __str__(self) -> str:
        return self.router.prefix


class RestAPI(APIMixin):
    """Main class for create RESTful-API."""

    router: Union[APIRouter, FastAPI]

    def __init__(self, fastapi_app: FastAPI, prefix: Optional[str] = "/api"):
        """
        Init class.

        Parameters
        ----------
        fastapi_app: instance of FastAPI
        prefix: Default prefix in url path.
        """
        self._fastapi: FastAPI = fastapi_app
        self._prefix: str = prefix
        self._versions: Dict[str, APIVersion] = {}
        self.__init_main_router__()

    def __getitem__(self, item: str) -> Optional[APIVersion]:
        """
        Get instance API by prefix version.

        Parameters
        ----------
        item: Prefix version

        Returns
        -------
        Instance API or None
        """
        prefix = self._strip_prefix(item)
        return self._versions.get(f"/{prefix}")

    def __init_main_router__(self) -> None:
        """
        Init main router.

        Returns
        -------
        None
        """
        prefix = self._strip_prefix(self._prefix)
        if prefix:
            router = APIRouter(prefix=f"/{prefix}")
        else:
            router = self._fastapi
        self.router = router

    @property
    def versions(self) -> Dict[str, APIVersion]:
        """Versions map"""
        return self._versions

    def apply(self) -> None:
        """
        Include new api urls to FastAPI app.

        Returns
        -------
        None
        """
        for router in self._versions.values():
            self.router.include_router(router.router)
        if isinstance(self.router, APIRouter):
            self._fastapi.include_router(self.router)

    def include_api_version(self, api_version: APIVersion) -> None:
        """
        Include API version to main router.

        Parameters
        ----------
        api_version
            Instance of APIVersion with included resources.
        """
        prefix = api_version.router.prefix
        if prefix in self._versions:
            raise AssertionError(f"This version is exist: {prefix}")
        self._versions[prefix] = api_version
        self.router.include_router(api_version.router)
