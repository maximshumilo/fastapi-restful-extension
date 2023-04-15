from unittest.mock import patch

import pytest
from fastapi import FastAPI

from fastapi_restful import RESTExtension, RestAPI


class TestRESTExtension:
    def test__init__success(self):
        api = RESTExtension()
        assert api.path == "/api"
        assert api.rest_api_map == {}


    def test__init__set_prefix__success(self):
        prefix = '/custom'
        api = RESTExtension(path=prefix)
        assert api.path == prefix
        assert api.rest_api_map == {}

    def test__get_item__success(self):
        key, obj = 'key', 'obj'
        api = RESTExtension()
        api.rest_api_map[key] = obj
        get_obj = api[key]
        assert get_obj == obj

    def test__get_item__not_found(self):
        key = 'unknown_key'
        api = RESTExtension()
        get_obj = api[key]
        assert get_obj is None
        assert key not in api.rest_api_map

    def test__mount_to_app__success(self):
        api = RESTExtension()
        app = FastAPI()
        with patch.object(app, 'mount') as mock:
            api.mount_to_app(fastapi_app=app)
        mock.assert_called()

    def test__add_api__success(self):
        rest_api = RestAPI(path='/test')
        api = RESTExtension()
        with patch.object(api.app, 'mount') as mock:
            api.add_api(api=rest_api)
        mock.assert_called_with(path=rest_api.path, app=rest_api.app)
        assert rest_api.path in api.rest_api_map

    def test__add_api__is_exist(self):
        rest_api = RestAPI(path='/test')
        api = RESTExtension()
        api.rest_api_map[rest_api.path] = rest_api
        with patch.object(api.app, 'mount') as mock, pytest.raises(AssertionError):
            api.add_api(api=rest_api)
        assert rest_api.path in api.rest_api_map
        mock.assert_not_called()
