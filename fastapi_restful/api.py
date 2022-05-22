from typing import Type, Optional, Dict

from fastapi import FastAPI, APIRouter

from .resource import Resource


class APIMixin:
    router: APIRouter

    @property
    def url_map(self) -> dict:
        return {route.path: route for route in self.router.routes}

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
        self.router.include_router(res.router)


class API(APIMixin):
    """
    A class specific version API.
    """

    def __init__(self, prefix: str):
        self.router = APIRouter(prefix=prefix)

    def __str__(self):
        return f'API: {self.router.prefix}'


class RestAPI(APIMixin):
    """Main class for create RESTful-API."""
    fastapi: FastAPI

    _versions: Dict[str, API]

    def __init__(self, fastapi_app: FastAPI = None, prefix: str = '/api'):
        """
        Init class.

        Parameters
        ----------
        fastapi_app: instance of FastAPI
        prefix: Default prefix in url path.
        """
        self.fastapi = fastapi_app
        self.router = APIRouter(prefix=prefix)
        self.fastapi.include_router(self.router)
        self._versions = {}

    def __getitem__(self, item: str) -> Optional[API]:
        """
        Get instance API by prefix version.

        Parameters
        ----------
        item: Prefix version

        Returns
        -------
        Instance API or None
        """
        return self._versions.get(item)

    @property
    def versions(self) -> Dict[str, API]:
        """Versions map"""
        return self._versions

    def create_version(self, prefix: str) -> API:
        """Create new version API"""
        if prefix in self._versions:
            raise AssertionError(f'This version is exist: {prefix}')
        api_spec_ver = API(prefix)
        self._versions[prefix] = api_spec_ver
        self.router.include_router(api_spec_ver.router)
        return api_spec_ver
