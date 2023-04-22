from inspect import signature

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture

from fastapi_restful import Resource, RESTExtension

app = FastAPI()


@fixture
def resource_type():
    class TestResource(Resource):
        tag = 'my_tag'
        path = "/test"

    return TestResource

@fixture
def resource_instance():
    return Resource()

@fixture
def signature_with_value():
    def my_handler(my_arg='value'):
        pass

    return signature(my_handler)


@fixture
def fastapi_test_client():
    return TestClient(app)


@fixture
def rest_api_instance():
    return RESTExtension()


@fixture
def api_version_instance():
    return RESTExtension(path="/v1")
