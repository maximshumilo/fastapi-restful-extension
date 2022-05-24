from typing import Type, Optional, Dict, Union

from fastapi import FastAPI, APIRouter

from .resource import Resource


class APIMixin:
    router: APIRouter

    @staticmethod
    def _strip_prefix(prefix: Optional[str]) -> str:
        return prefix.strip('/') if prefix is not None else ''

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
        resource: Type of Resource
        path: Resource path

        Returns
        -------
        None
        """
        res = resource(path)
        self.router.include_router(res.router)


class APIVersion(APIMixin):
    """
    A class specific version API.
    """

    def __init__(self, version_prefix: str):
        prefix = self._strip_prefix(version_prefix)
        self.router = APIRouter(prefix=f'/{prefix}')

    def __str__(self) -> str:
        return self.router.prefix


class RestAPI(APIMixin):
    """Main class for create RESTful-API."""
    router: Union[APIRouter, FastAPI]

    _fastapi: FastAPI
    _prefix: str
    _versions: Dict[str, APIVersion]

    def __init__(self, fastapi_app: FastAPI, prefix: Optional[str] = '/api'):
        """
        Init class.

        Parameters
        ----------
        fastapi_app: instance of FastAPI
        prefix: Default prefix in url path.
        """
        self._fastapi = fastapi_app
        self._prefix = prefix
        self._versions = {}
        self.__init_router__()

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
        return self._versions.get(f'/{prefix}')

    def __init_router__(self) -> None:
        """
        Init router.

        Returns
        -------
        None
        """
        prefix = self._strip_prefix(self._prefix)
        if prefix:
            router = APIRouter(prefix=f'/{prefix}')
        else:
            router = self._fastapi
        self.router = router

    @property
    def versions(self) -> Dict[str, APIVersion]:
        """Versions map"""
        return self._versions

    def create_version(self, prefix: str) -> APIVersion:
        """
        Create new version API.

        Parameters
        ----------
        prefix: Prefix version

        Returns
        -------
        APIVersion instance
        """
        if prefix in self._versions:
            raise AssertionError(f'This version is exist: {prefix}')
        api_spec_ver = APIVersion(prefix)
        self._versions[prefix] = api_spec_ver
        self.router.include_router(api_spec_ver.router)
        return api_spec_ver

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
