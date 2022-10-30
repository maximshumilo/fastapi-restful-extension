from inspect import Parameter, signature
from typing import Callable


def is_overridden_func(target_func) -> bool:
    """
    Check if the function is overridden in child class.

    Parameters
    ----------
    target_func: Target function

    Returns
    -------
    True/False
    """
    child_instance = target_func.__self__
    func_of_parent = getattr(super(type(child_instance), child_instance), target_func.__name__)
    return target_func.__func__ != func_of_parent.__func__


def route_settings(**kwargs) -> Callable:
    """
    Decorator for forwarding 'kwargs' to the 'add_api_route' method of the 'APIRouter` instance.

    Parameters
    ----------
    kwargs: Kwargs for add_api_route.
            See descriptions for all kwargs in `fastapi.APIRouter.add_api_route`.

    Returns
    -------
    Func with new signature.
    """

    def decorator(func):
        route_kwargs_param = Parameter(name="route_kwargs", kind=Parameter.POSITIONAL_OR_KEYWORD, default=kwargs)
        sign = signature(func)
        old_params = list(sign.parameters.values())
        old_params.append(route_kwargs_param)
        func.__signature__ = sign.replace(parameters=old_params)
        return func

    return decorator
