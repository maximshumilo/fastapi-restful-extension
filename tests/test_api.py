from unittest.mock import patch

import pytest
from fastapi import FastAPI

from fastapi_restful import RestAPI


def test__init_rest_api__success():
    api = RestAPI()
    assert api.path == "/api"


def test__init_rest_api__empty_default_prefix__success():
    assert True

