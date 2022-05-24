from fastapi_restful import route_settings


def test_route_settings(rest_api_for_test, resource_for_test):
    summary = "TestSummary"

    @route_settings(summary='TestSummary')
    def get(self):
        return {}

    resource_for_test.get = get
    resource_prefix = '/test'
    rest_api_for_test.add_resource(resource_for_test, resource_prefix)
    assert rest_api_for_test.router.routes[0].summary == summary
