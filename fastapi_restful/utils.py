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
