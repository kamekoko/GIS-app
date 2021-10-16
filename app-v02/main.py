from fastapi import FastAPI
# import pyproj

import readData as rd
import epsg as e
# import transformCrs as tc

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/readTestData/")
async def readTestGeojson():
    return rd.read_geojson('./data/farm_komatsu.geojson')

@app.get("/transformCrs/{data_id}/to/{epsg}")
async def transformCrs(data_id, epsg):
    path = './data/' + data_id + '.geojson'
    before_epsg = e.getEpsg(data_id)
    r = tc.transform(path, before_epsg, epsg)
    return r
