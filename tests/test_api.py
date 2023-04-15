from unittest.mock import patch

import pytest
from fastapi import FastAPI

from fastapi_restful import Resource, RestAPI, RESTExtension


class TestRESTExtension:
    def test__init__success(self):
        api = RESTExtension()
        assert api.path == "/api"
        assert api.rest_api_map == {}

    def test__init__set_prefix__success(self):
        prefix = "/custom"
        api = RESTExtension(path=prefix)
        assert api.path == prefix
        assert api.rest_api_map == {}

    def test__get_item__success(self):
        key, obj = "key", "obj"
        api = RESTExtension()
        api.rest_api_map[key] = obj
        get_obj = api[key]
        assert get_obj == obj

    def test__get_item__not_found(self):
        key = "unknown_key"
        api = RESTExtension()
        get_obj = api[key]
        assert get_obj is None
        assert key not in api.rest_api_map

    def test__mount_to_app__success(self):
        api = RESTExtension()
        app = FastAPI()
        with patch.object(app, "mount") as mock:
            api.mount_to_app(fastapi_app=app)
        mock.assert_called()

    def test__add_api__success(self):
        rest_api = RestAPI(path="/test")
        api = RESTExtension()
        with patch.object(api.app, "mount") as mock:
            api.add_api(api=rest_api)
        mock.assert_called_with(path=rest_api.path, app=rest_api.app)
        assert rest_api.path in api.rest_api_map

    def test__add_api__is_exist(self):
        rest_api = RestAPI(path="/test")
        api = RESTExtension()
        api.rest_api_map[rest_api.path] = rest_api
        with patch.object(api.app, "mount") as mock, pytest.raises(AssertionError):
            api.add_api(api=rest_api)
        assert rest_api.path in api.rest_api_map
        mock.assert_not_called()


class TestRestAPI:
    def test__init__success(self):
        path = "/path"
        api = RestAPI(path=path)
        assert api.path == path

    def test__init__success__without_slash(self):
        path = "path"
        api = RestAPI(path=path)
        assert api.path.startswith("/")

    def test__str__equal_path(self):
        path = "path"
        api = RestAPI(path=path)
        assert str(api) == api.path

    def test__strip_path__success(self):
        path = "/path"
        path = RestAPI._strip_path(path=path)
        assert not path.startswith("/")
        assert "/" not in path

    def test__strip_path__success__path_is_none(self):
        api = RestAPI(path="")
        with patch.object(api.app, "include_router") as mock:
            api.add_resource(resource=Resource, path="/resource_path")
        mock.assert_called()
