from inspect import getmembers, ismethod, Parameter, Signature, signature
from typing import List, Callable

from fastapi import APIRouter, HTTPException, params


class HTTPMethods:
    _HTTP_METHODS: tuple = ('head', 'options', 'get', 'post', 'patch', 'put', 'delete')

    def _get_route_handlers(self) -> List[tuple]:
        filter_obj = filter(
            lambda x: x[0] in self._HTTP_METHODS and self._is_overridden_func(x[1]),
            getmembers(self, predicate=ismethod)
        )
        return list(filter_obj)

    def _is_overridden_func(self, func_of_child):
        func_of_parent = getattr(super(type(self), self), func_of_child.__name__)
        return func_of_child.__func__ != func_of_parent.__func__

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


class Resource(HTTPMethods):

    router: APIRouter
    tag: str = None
    endpoint: str = None

    def __init__(self, endpoint: str = None):
        if self.tag is None:
            self.tag = self.__class__.__name__
        if endpoint is not None:
            self.endpoint = endpoint
        self.__init_router__()

    def __init_router__(self):
        self.router = APIRouter(prefix=self.endpoint, tags=[self.tag])
        self.__include_methods__()

    def __include_methods__(self):
        for method, handler in self._get_route_handlers():
            kwargs = self.__get_kwargs__(handler)
            func = self.__replace_signature__(handler)
            self.router.add_api_route(path='', endpoint=func, methods=[method], **kwargs)

    @staticmethod
    def __get_kwargs__(func: Callable):
        sign = signature(func)
        return {
            k: v.default
            for k, v in sign.parameters.items()
            if v.default is not Parameter.empty and not isinstance(v.default, params.Query)
        }

    def __replace_signature__(self, func: Callable):
        def new_func(*args, **kwargs):
            return func(*args, **kwargs)
        sign = signature(func)
        new_params = self.__gen_new_params__(sign)
        new_func.__signature__ = sign.replace(parameters=new_params)
        return new_func

    def __gen_new_params__(self, sign: Signature):
        old_params = list(sign.parameters.values())
        new_params = [p.replace(kind=Parameter.POSITIONAL_OR_KEYWORD) for p in old_params
                      if p.name in self._required_args or isinstance(p.default, params.Query)]
        return new_params

    @property
    def _required_args(self):
        return [item.strip('{}') for item in self.endpoint.split('/') if item.startswith('{') and item.endswith('}')]
