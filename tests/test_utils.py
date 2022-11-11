from fastapi_restful import route_settings


def test_route_settings(rest_api_instance, resource_type):
    summary = "TestSummary"

    @route_settings(summary="TestSummary")
    def get(self):
        return {}

    resource_type.get = get
    resource_prefix = "/test"
    rest_api_instance.add_resource(resource_type, resource_prefix)
    assert rest_api_instance.router.routes[0].summary == summary
