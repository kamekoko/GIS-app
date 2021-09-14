from typing import Optional
from enum import Enum
from fastapi import FastAPI
import numpy as np

from get_json import get_json
import xy2ll

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI(
    title='Spatial Data Integration Platform v0.1'
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/get_test/")
async def get_test_json():
    return get_json('../data/input/test.geojson')

# @app.get("/get_farmland")
# async def get_farmland(shpTogeojson: bool = False):
#     if shpTogeojson:
#         #
#     else:
#         return {"message": "This API provides farmland data in geojson format by setting the parameter shpToGeojson=True."}

@app.get("/xy2ll/")
async def xy2ll_farmland():
    return xy2ll.xy2ll('../data/output/out-farmland.geojson')



# tutorial

# @app.get("/users/me")
# async def read_user_me():
#     return {"user_id": "the current user"}
#
# @app.get("/users/{user_id}")
# async def read_user(user_id: str):
#     return {"user_id": user_id}
#
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
#
# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update({"description": "This is an amazing item that has a long description"})
#     return item
#
# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name == ModelName.alexnet:
#         return {"model_name": model_name, "message": "DeepLearning FTW!"}
#     if model_name == ModelName.lenet:
#         return {"model_name": model_name, "message": "LeCNN all the images"}
#     return {"model_name": model_name, "message": "Have some residuals"}
