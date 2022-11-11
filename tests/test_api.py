from unittest.mock import patch

import pytest
from fastapi import FastAPI

from fastapi_restful import RestAPI


def test__init_rest_api__success():
    app = FastAPI()
    api = RestAPI(fastapi_app=app)
    assert api._fastapi is app
    assert api.router.prefix == "/api"


def test__init_rest_api__empty_default_prefix__success():
    app = FastAPI()
    api = RestAPI(fastapi_app=app, prefix=None)
    assert api._fastapi is app
    assert not hasattr(api.router, "prefix")


@patch("fastapi_restful.resource.Resource")
def test__add_resource__success(resource_mock, rest_api_instance):
    assert rest_api_instance.add_resource(resource_mock) is None


def test__get_item__success(rest_api_instance, api_version_instance):
    assert rest_api_instance.versions == {}
    prefix = api_version_instance.router.prefix
    rest_api_instance._versions[prefix] = api_version_instance
    assert rest_api_instance[prefix] is api_version_instance


def test__str__success(api_version_instance):
    prefix = api_version_instance.router.prefix
    assert str(api_version_instance) == prefix


def test__url_map__success(rest_api_instance, resource_type):
    def get(self):
        return {}

    resource_type.get = get
    rest_api_instance.add_resource(resource_type)
    base_prefix = rest_api_instance.router.prefix
    path = f"{base_prefix}{resource_type.path}"
    assert rest_api_instance.urls.get(path) is not None


def test__apply__success(rest_api_instance, resource_type, api_version_instance):
    def get(self):
        return {}

    resource_type.get = get
    api_version_instance.add_resource(resource_type)
    rest_api_instance.include_api_version(api_version_instance)
    assert rest_api_instance.apply() is None


def test__call_http_methods__success(resource_type):
    for method_name in resource_type._HTTP_METHODS:
        method = getattr(resource_type, method_name)
        assert method is not None
        method(resource_type)


def test__include_api_version__failed__prefix_is_exist(rest_api_instance, api_version_instance):
    expected_error_msg = "This version is exist: /v1"
    rest_api_instance._versions[api_version_instance.router.prefix] = api_version_instance
    exc = pytest.raises(AssertionError, rest_api_instance.include_api_version, api_version_instance)
    assert str(exc.value) == expected_error_msg
