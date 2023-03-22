This extension allows you to create separate versions of the api. 
At the same time, the prefix specified during version initialization is added to the url of the main API.

---

### Creating second version API
As an example, let's add a version to the previous example from the [Minimal API](minimal-api.md) section.

```python title="first_api.py" linenums="1" hl_lines="15-17 20 21 22"
from fastapi import FastAPI
from uvicorn import run

from fastapi_restful import RESTExtension, Resource, RESTExtension

app = FastAPI()
api = RESTExtension(app)


class FirstResource(Resource):
    def get(self):
        return {'first': 'resource'}


class SecondResource(Resource):
    def get(self):
        return {'second': 'resource'}


v2 = RESTExtension(prefix='v2')
v2.add_resource(SecondResource, path='/second-resource')
api.add_rest_api()

api.add_resource(FirstResource, path='/first-resource')
api.apply()

if __name__ == '__main__':
    run('first_api:app')
```
The `SecondResource` class is declared by analogy with `FirstResource`.

A new version of the API with the prefix `v2` has been created and the `SecondResource` class and the path by which it can be accessed have been added to it

As a result, two routes will be registered:

- `GET /api/first-resource/`
- `GET /api/v2/second-resource/`

!!! note
    Нou can get an instance of `RESTExtension` using the `__getitem__` method from the `RESTExtension` instance by a prefix.

    ```python
    >>> api_v2 = api.create_version('v2')
    >>> api['v2'] is api_v2
    True
    ```
