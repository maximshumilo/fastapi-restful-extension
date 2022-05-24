import pytest
from fastapi import APIRouter


def test_init_resource_default_tag(resource_for_test):
    instance = resource_for_test()
    assert instance.tag == resource_for_test.__name__


def test_init_resource_custom_tag(resource_for_test):
    custom_tag = 'Test custom tag'
    resource_for_test.tag = custom_tag
    instance = resource_for_test()
    assert instance.tag == custom_tag


def test_init_resource_default_path(resource_for_test):
    instance = resource_for_test()
    assert instance.path == ''


def test_init_resource_custom_path(resource_for_test):
    custom_path = '/my/path'
    instance = resource_for_test(path=custom_path)
    assert instance.path == custom_path


def test_init_resource_init_router(resource_for_test):
    instance = resource_for_test()
    assert instance.router is not None
    assert isinstance(instance.router, APIRouter)
    assert instance.router.tags == [resource_for_test.__name__]
    assert instance.router.prefix == resource_for_test.path


def test_init_resource_include_methods(resource_for_test):
    def get(self, **kwargs):
        return {}

    instance_before = resource_for_test()
    assert len(instance_before.router.routes) == 0
    resource_for_test.get = get
    instance = resource_for_test()
    assert len(instance.router.routes) == 1


def test_resource_required_args_in_path(resource_for_test):
    instance = resource_for_test(path='/api/{path_arg}')
    assert instance._required_args == ['path_arg']


def test_execute_func_with_new_signature(resource_for_test):
    output = {}

    def get(self, **kwargs):
        return output

    resource_for_test.get = get
    instance = resource_for_test()
    new_func = instance.__replace_signature__(instance.get)
    assert new_func() == output


@pytest.mark.asyncio
async def test_execute_func_with_new_signature_async(resource_for_test):
    output = {}

    async def get(self, **kwargs):
        return output

    resource_for_test.get = get
    instance = resource_for_test()
    new_func = instance.__replace_signature__(instance.get)
    assert await new_func() == output
