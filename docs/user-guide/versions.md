This extension allows you to create separate versions of the api. 
At the same time, the prefix specified during version initialization is added to the url of the main API.

---

### Creating second version API
As an example, let's add a version to the previous example from the `A minimal API` section.


```python title="first_api.py" linenums="1" hl_lines="17-19 22 23"
from fastapi import FastAPI
from fastapi_restful import RestAPI, Resource
from uvicorn import run

app = FastAPI()
api = RestAPI(app)


class FirstResource(Resource):
    def get(self):
        return {'first': 'resource'}


api.add_resource(FirstResource, path='/first-resource')


class SecondResource(Resource):
    def get(self):
        return {'second': 'resource'}

    
v2 = api.create_version('v2')
v2.add_resource(SecondResource, path='/second-resource')
api.apply()

if __name__ == '__main__':
    run('first_api:app')
```
The SecondResource class is declared by analogy with FirstResource.

A new version of the API with the prefix `v2` has been created and the `SecondResource` class and the path by which it can be accessed have been added to it

As a result, two routes will be registered:

- `GET /api/first-resource/`
- `GET /api/v2/second-resource/`

---

### Get APIVersion instance from RestAPI