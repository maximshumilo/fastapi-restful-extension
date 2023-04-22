from inspect import Parameter, Signature, getmembers, iscoroutinefunction, ismethod, signature
from typing import Any, Callable, Dict, List, Tuple

from fastapi import APIRouter

from .utils import is_overridden_func


class ManageSignature:
    """A class for interacting with a function signature."""

    _required_args: List[str]

    @staticmethod
    def __get_default_value_of_route_kwargs__(func: Callable) -> Dict[str, Any]:
        """
        Get default values of route_kwargs from target func.

        Parameters
        ----------
        func:
            Target func

        Returns
        -------
        Default value of param `route_kwargs` from target func.
        """
        sign = signature(func)
        res = next(filter(lambda x: x.name == "route_kwargs", sign.parameters.values()), {})
        return getattr(res, 'default', {})

    def _create_new_route_handler(self, func: Callable) -> Callable:
        """
        Create new route handler function with new kwargs

        Parameters
        ----------
        func: Callable
            Source func

        Returns
        -------
        New function with new kwargs.
        """

        def sync_route_handler(*args, **kwargs):
            return func(*args, **kwargs)

        async def async_route_handler(*args, **kwargs):
            return await func(*args, **kwargs)

        new_func = async_route_handler if iscoroutinefunction(func) else sync_route_handler
        sign = signature(func)
        new_params = self.__generate_new_params__(sign)
        new_func.__signature__ = sign.replace(parameters=new_params)
        return new_func

    @staticmethod
    def __generate_new_params__(sign: Signature) -> List[Parameter]:
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
        return [p.replace(kind=Parameter.POSITIONAL_OR_KEYWORD) for p in old_params if p.name != "route_kwargs"]


class HTTPMethods:
    """The supported HTTP methods are described here."""

    _HTTP_METHODS: tuple = ("head", "options", "get", "post", "patch", "put", "delete")

    def _get_overridden_route_handlers(self) -> List[Tuple[str, Callable]]:
        """
        Get route handler functions.

        Returns
        -------
        List with data o route handler methods.
        """
        filter_obj = filter(
            lambda x: x[0] in self._HTTP_METHODS and is_overridden_func(x[1]), getmembers(self, predicate=ismethod)
        )
        return list(filter_obj)

    def head(self, **kwargs):
        ...

    def options(self, **kwargs):
        ...

    def get(self, **kwargs):
        ...

    def post(self, **kwargs):
        ...

    def patch(self, **kwargs):
        ...

    def put(self, **kwargs):
        ...

    def delete(self, **kwargs):
        ...


class Resource(HTTPMethods, ManageSignature):
    """This class is designed to implement CRUD methods of a specific api resource with FastAPI."""

    router: APIRouter
    tag: str = None
    path: str = ""

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

        Get kwargs from implemented method (only for route), and replace signature of route func,
        then add api route to router.

        Returns
        -------
        None
        """
        for method_name, method_callable in self._get_overridden_route_handlers():
            route_kwargs = self.__get_default_value_of_route_kwargs__(method_callable)
            kwargs = {"summary": method_name, **route_kwargs}
            route_handler = self._create_new_route_handler(method_callable)
            self.router.add_api_route(path="", endpoint=route_handler, methods=[method_name.capitalize()], **kwargs)

    @property
    def _required_args(self) -> List[str]:
        """
        Get required arg names from path of this Resource instance.

        Returns
        -------
        List with required arg names.
        """
        return [item.strip("{}") for item in self.path.split("/") if item.startswith("{") and item.endswith("}")]
