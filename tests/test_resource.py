from inspect import Signature
from typing import Type
from unittest.mock import patch

import pytest

from fastapi_restful.resource import ManageSignature, Resource, HTTPMethods


class TestManageSignature:

    def test__get_route_kwargs__success(self):
        default_value = 1

        def my_handler(route_kwargs=default_value):
            pass

        result = ManageSignature.__get_default_value_of_route_kwargs__(func=my_handler)
        assert result == default_value

    def test__get_route_kwargs__success__empty(self):
        def my_handler():
            pass

        result = ManageSignature.__get_default_value_of_route_kwargs__(func=my_handler)
        assert result == {}

    def test__create_new_route_handler__success_sync(self, resource_instance: Resource):
        def my_handler():
            pass

        with patch.object(resource_instance, '__generate_new_params__', return_value=[]):
            result = resource_instance._create_new_route_handler(func=my_handler)
        assert result.__name__ == 'sync_route_handler'
        assert result() is None

    @pytest.mark.asyncio
    async def test__create_new_route_handler__success_async(self, resource_instance: Resource):
        async def my_handler():
            pass

        with patch.object(resource_instance, '__generate_new_params__', return_value=[]):
            result = resource_instance._create_new_route_handler(func=my_handler)
        assert result.__name__ == 'async_route_handler'
        assert await result() is None

    def test__generate_new_params__success(self, signature_with_value: Signature):
        result = ManageSignature.__generate_new_params__(sign=signature_with_value)
        assert result
        assert result[0].name == 'my_arg'
        assert result[0].default == 'value'


class TestHTTPMethods:

    def test__get_overridden_route_handlers__success(self):

        class MyClass(HTTPMethods):
            def get(self, **kwargs):
                pass

        instance = MyClass()
        result = instance._get_overridden_route_handlers()
        assert instance.get == result[0][1]

    def test__get_overridden_route_handlers__failed__not_http(self):

        class MyClass(HTTPMethods):
            def custom_method(self, **kwargs):
                pass

        instance = MyClass()
        result = instance._get_overridden_route_handlers()
        assert not result

    def test__call_abs_http_methods__success(self):
        class MyClass(HTTPMethods):
            pass
        instance = MyClass()


        for http_method in instance._HTTP_METHODS:
            method = getattr(instance, http_method)
            result = method()
            assert not result


class TestResource:

    def test__init__success(self):
        with patch.object(Resource, '__init_router__') as init_router__mock:
            instance = Resource()
        assert not instance.tag == Resource.tag
        assert instance.tag == Resource.__name__
        assert instance.path == ''
        init_router__mock.assert_called()

    def test__init__success__with_tag(self, resource_type: Type[Resource]):
        with patch.object(resource_type, '__init_router__') as init_router__mock:
            instance = resource_type()
        assert instance.tag == resource_type.tag
        assert instance.path == resource_type.path
        init_router__mock.assert_called()

    def test__init_router__success(self, resource_instance: Resource):
        with patch.object(resource_instance, '__include_methods__') as init_router__mock:
            before_router = resource_instance.router
            resource_instance.__init_router__()
            after_router = resource_instance.router
        assert before_router is not after_router
        init_router__mock.assert_called()

    def test__include_methods__success(self, resource_instance: Resource):
        def my_handler():
            pass
        overridden_handlers = [('get', my_handler)]
        with patch.object(resource_instance, '_get_overridden_route_handlers', return_value=overridden_handlers), \
             patch.object(resource_instance, '__get_default_value_of_route_kwargs__', return_value={}) as mock_1, \
             patch.object(resource_instance, '_create_new_route_handler') as mock_2, \
             patch.object(resource_instance.router, 'add_api_route') as mock_3:
            resource_instance.__include_methods__()
        mock_1.assert_called()
        mock_2.assert_called_with(my_handler)
        mock_3.assert_called()
