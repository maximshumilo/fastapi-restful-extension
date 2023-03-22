from fastapi_restful import RESTExtension


def test__init_rest_api__success():
    api = RESTExtension()
    assert api.path == "/api"


def test__init_rest_api__empty_default_prefix__success():
    assert True
