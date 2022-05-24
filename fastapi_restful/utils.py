from inspect import Parameter, signature


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


def route_settings(**kwargs):
    def decorator(func):
        route_kwargs_param = Parameter(name='route_kwargs', kind=Parameter.POSITIONAL_OR_KEYWORD, default=kwargs)
        sign = signature(func)
        old_params = list(sign.parameters.values())
        old_params.append(route_kwargs_param)
        func.__signature__ = sign.replace(parameters=old_params)
        return func
    return decorator
