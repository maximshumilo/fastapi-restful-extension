Here are the steps to create a minimal api for "FastAPI" using FastAPI-RESTful-Extension.

---

### Install `uvicorn` for run server.

```console 
$ pip install uvicorn
Collecting uvicorn
  Using cached uvicorn-0.17.6-py3-none-any.whl (53 kB)
...
...
...
Installing collected packages: h11, asgiref, uvicorn
Successfully installed asgiref-3.5.2 h11-0.13.0 uvicorn-0.17.6
```

---

### Create a file `first_api.py` and fill it with the following contents.

```python title="first_api.py" linenums="1" hl_lines="5 6"
from fastapi import FastAPI
from fastapi_restful import RESTExtension, Resource
from uvicorn import run

app = FastAPI()
api = RESTExtension(app)


class FirstResource(Resource):
    def get(self):
        return {'first': 'resource'}


api.add_resource(FirstResource, path='/first-resource')
api.apply()

if __name__ == '__main__':
    run('first_api:app')
```

The FastAPI application will be created and routes with methods described in the `FirstResource` class will be connected.

!!! note

    `/api/...` - this prefix is added by default to the `RESTExtension` instance. <br>
    If you don't need it, specify `prefix=None` when initializing `RESTExtension`

```python title="first_api.py" linenums="1" hl_lines="9-11 14 15"
from fastapi import FastAPI
from fastapi_restful import RESTExtension, Resource
from uvicorn import run

app = FastAPI()
api = RESTExtension(app)


class FirstResource(Resource):
    def get(self):
        return {'first': 'resource'}


api.add_resource(FirstResource, path='/first-resource')
api.apply()

if __name__ == '__main__':
    run('first_api:app')
```

The `FirstResource` class inherited from `Resource` is declared, in it declares a method for processing the corresponding http request.

Then this class with its URLs passed to `api.add_resource()`

The `api.apply()` method include all declared routes from `api` to FastAPI

As a result one route will be registered - `GET /api/first-resource/`

---

### Run api.

```console
$ python first_api.py

INFO:     Started server process [71507]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

### Check created api.

```console
$ curl http://127.0.0.1:8000/api/first-resource
{"first":"resource"}
```
