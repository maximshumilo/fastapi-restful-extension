from inspect import signature

from fastapi_restful.utils import is_overridden_func, route_settings


def test__is_overridden_func__success():
    class Source:
        def foo(self):
            pass

    class MyClass(Source):
        def foo(self):
            pass

    instance = MyClass()
    result = is_overridden_func(target_func=instance.foo)
    assert result is True


def test__is_overridden_func__fail():
    class Source:
        def foo(self):
            pass

    class MyClass(Source):
        pass

    instance = MyClass()
    result = is_overridden_func(target_func=instance.foo)
    assert result is False


def test__decorator_route_settings__success():
    @route_settings(my_arg="my_value")
    def foo():
        pass

    sign_of_foo = signature(foo)
    assert sign_of_foo.parameters.get("route_kwargs")
