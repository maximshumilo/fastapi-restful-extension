from fastapi import FastAPI

from fastapi_restful import Api


def test_init_api_with_fastapi():
    app = FastAPI()
    api = Api(fastapi_app=app)
    assert api.fastapi is app


def test_init_api_without_fastapi():
    api = Api()
    assert api.fastapi is None


def test_init_fastapi():
    app = FastAPI()
    api = Api()
    api.init_fastapi(app)
    assert api.fastapi is app


def test_add_resource(resource_for_test, api_for_test):
    api_for_test.add_resource(resource_for_test)
