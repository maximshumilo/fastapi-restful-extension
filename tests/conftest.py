from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture

from fastapi_restful import Resource, RestAPI

app = FastAPI()


@fixture
def resource_for_test():
    class TestResource(Resource):
        pass
    return TestResource


@fixture
def fastapi_test_client():
    return TestClient(app)


@fixture
def rest_api_for_test():
    return RestAPI(app)
