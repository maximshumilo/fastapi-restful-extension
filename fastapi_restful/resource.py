from inspect import getmembers, ismethod, Parameter, Signature, signature
from typing import List, Callable, Tuple, Dict, Any

from fastapi import APIRouter, HTTPException, params

from .utils import is_overridden_func


class ManageSignature:
    """A class for interacting with a function signature."""

    _required_args: List[str]

    @staticmethod
    def __get_kwargs__(func: Callable) -> Dict[str, Any]:
        """
        Get keyword names and default values from func.
        Skip item If default value is Query instance of FastAPI.

        Parameters
        ----------
        func: Target func

        Returns
        -------
        Kwargs
        """
        sign = signature(func)
        return {
            k: v.default
            for k, v in sign.parameters.items()
            if v.default is not Parameter.empty and not isinstance(v.default, params.Query)
        }

    def __replace_signature__(self, func: Callable) -> Callable:
        """
        Decorator for set new signature.

        Parameters
        ----------
        func: Target func

        Returns
        -------
        New function with new signature.
        """

        def new_func(*args, **kwargs):
            return func(*args, **kwargs)
        sign = signature(func)
        new_params = self.__gen_new_params__(sign)
        new_func.__signature__ = sign.replace(parameters=new_params)
        return new_func

    def __gen_new_params__(self, sign: Signature) -> List[Parameter]:
        """
        Generate list with new params for signature.

        Parameters
        ----------
        sign: Signature

        Returns
        -------
        List with new params.
        """
        old_params = list(sign.parameters.values())
        new_params = [p.replace(kind=Parameter.POSITIONAL_OR_KEYWORD) for p in old_params
                      if p.name in self._required_args or isinstance(p.default, params.Query)]
        return new_params


class HTTPMethods:
    """The supported HTTP methods are described here."""

    _HTTP_METHODS: tuple = ('head', 'options', 'get', 'post', 'patch', 'put', 'delete')

    def _get_route_handlers(self) -> List[Tuple[str, Callable]]:
        """
        Get route handler functions.

        Returns
        -------
        List with data o route handlers.
        """
        filter_obj = filter(
            lambda x: x[0] in self._HTTP_METHODS and is_overridden_func(x[1]), getmembers(self, predicate=ismethod)
        )
        return list(filter_obj)

    def head(self):
        raise HTTPException(status_code=405, detail="Method Not Allowed")

    def options(self):
        raise HTTPException(status_code=405, detail="Method Not Allowed")

    def get(self, **kwargs):
        raise HTTPException(status_code=405, detail="Method Not Allowed")

    def post(self, **kwargs):
        raise HTTPException(status_code=405, detail="Method Not Allowed")

    def patch(self):
        raise HTTPException(status_code=405, detail="Method Not Allowed")

    def put(self):
        raise HTTPException(status_code=405, detail="Method Not Allowed")

    def delete(self):
        raise HTTPException(status_code=405, detail="Method Not Allowed")


class Resource(HTTPMethods, ManageSignature):
    """This class is designed to implement CRUD methods of a specific api resource with FastAPI."""

    router: APIRouter
    tag: str = None
    path: str = ''

    def __init__(self, path: str = None):
        """
        Init Resource instance.
        If the value of the 'tag' attribute is not set. Then the value will be the name of the class instance.

        Parameters
        ----------
        path: Path for this resource
        """
        if self.tag is None:
            self.tag = self.__class__.__name__
        if path is not None:
            self.path = path
        self.__init_router__()

    def __init_router__(self) -> None:
        """
        Init APIRouter of FastAPI and include implemented methods.

        Returns
        -------
        None
        """
        self.router = APIRouter(prefix=self.path, tags=[self.tag])
        self.__include_methods__()

    def __include_methods__(self):
        """
        Include HTTP methods to router.

        Get kwargs from implemented method (only for route), and replace signature of route_handler,
        then add api route to router.

        Returns
        -------
        None
        """
        for method, handler in self._get_route_handlers():
            kwargs = self.__get_kwargs__(handler)
            route_handler = self.__replace_signature__(handler)
            self.router.add_api_route(path='', endpoint=route_handler, methods=[method], **kwargs)

    @property
    def _required_args(self) -> List[str]:
        """
        Get required arg names from path of this Resource instance.

        Returns
        -------
        List with required arg names.
        """
        return [item.strip('{}') for item in self.path.split('/') if item.startswith('{') and item.endswith('}')]
