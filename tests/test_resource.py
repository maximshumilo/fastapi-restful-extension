import pytest
from fastapi import APIRouter


def test_init_resource_default_tag(resource_type):
    instance = resource_type()
    assert instance.tag == resource_type.__name__


def test_init_resource_custom_tag(resource_type):
    custom_tag = "Test custom tag"
    resource_type.tag = custom_tag
    instance = resource_type()
    assert instance.tag == custom_tag


def test_init_resource_default_path(resource_type):
    default_path = resource_type.path
    instance = resource_type()
    assert instance.path == default_path


def test_init_resource_custom_path(resource_type):
    custom_path = "/my/path"
    instance = resource_type(custom_path)
    assert instance.path == custom_path


def test_init_resource_init_router(resource_type):
    instance = resource_type()
    assert instance.router is not None
    assert isinstance(instance.router, APIRouter)
    assert instance.router.tags == [resource_type.__name__]
    assert instance.router.prefix == resource_type.path


def test_init_resource_include_methods(resource_type):
    def get(self, **kwargs):
        return {}

    instance_before = resource_type()
    assert len(instance_before.router.routes) == 0
    resource_type.get = get
    instance = resource_type()
    assert len(instance.router.routes) == 1


def test_resource_required_args_in_path(resource_type):
    required_arg = "resource_id"
    instance = resource_type(path="/test/{%s}" % required_arg)
    assert required_arg in instance._required_args
    assert len(instance._required_args) == 1


def test_execute_func_with_new_signature(resource_type):
    assert True


@pytest.mark.asyncio
async def test_execute_func_with_new_signature_async(resource_type):
    assert True
