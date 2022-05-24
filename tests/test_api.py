import pytest
from fastapi import FastAPI

from fastapi_restful import RestAPI


def test_init_rest_api():
    app = FastAPI()
    api = RestAPI(fastapi_app=app)
    assert api._fastapi is app
    assert api.router.prefix == '/api'


def test_init_rest_api_empty_default_prefix():
    app = FastAPI()
    api = RestAPI(fastapi_app=app, prefix=None)
    assert api._fastapi is app


def test_add_resource(resource_for_test, rest_api_for_test):
    rest_api_for_test.add_resource(resource_for_test)


def test_create_version(rest_api_for_test):
    assert rest_api_for_test.versions == {}
    api = rest_api_for_test.create_version('/v1')
    assert rest_api_for_test.versions == {'/v1': api}


def test_create_version_failed_is_exist_prefix(rest_api_for_test):
    version_prefix = '/v1'
    assert rest_api_for_test.versions == {}
    api = rest_api_for_test.create_version(version_prefix)
    assert rest_api_for_test.versions == {version_prefix: api}
    pytest.raises(AssertionError, rest_api_for_test.create_version, version_prefix)


def test_get_version_by_prefix(rest_api_for_test):
    assert rest_api_for_test.versions == {}
    api = rest_api_for_test.create_version('/v1')
    assert rest_api_for_test['/v1'] is api


def test_str_of_instance(rest_api_for_test):
    prefix = '/v1'
    api = rest_api_for_test.create_version(prefix)
    assert str(api) == prefix


def test_url_map(rest_api_for_test, resource_for_test):
    def get(self):
        return {}
    resource_for_test.get = get
    resource_prefix = '/test'
    rest_api_for_test.add_resource(resource_for_test, resource_prefix)
    base_prefix = rest_api_for_test.router.prefix
    path = f'{base_prefix}{resource_prefix}'
    assert rest_api_for_test.urls.get(path) is not None


def test_apply(rest_api_for_test, resource_for_test):
    def get(self):
        return {}
    resource_for_test.get = get
    v1 = rest_api_for_test.create_version('v1')
    v1.add_resource(resource_for_test, '/test')
    rest_api_for_test.apply()
    assert True
