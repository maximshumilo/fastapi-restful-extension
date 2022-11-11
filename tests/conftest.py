from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture

from fastapi_restful import Resource, RestAPI, APIVersion

app = FastAPI()


@fixture
def resource_type():
    class TestResource(Resource):
        path = '/test'
        pass

    return TestResource


@fixture
def fastapi_test_client():
    return TestClient(app)


@fixture
def rest_api_instance():
    return RestAPI(app)


@fixture
def api_version_instance():
    return APIVersion(version_prefix='/v1')
