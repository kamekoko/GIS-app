from fastapi import FastAPI
import pyproj

import readData as rd
import epsg as e
import transformCrs as tc
import getPeopleCount as gpc
import getPaths as gp
import get_nearest as gn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/readTestData/")
async def readTestGeojson():
	return rd.read_geojson('./data/test.geojson')

@app.get("/transformCrs/{data_id}/to/{epsg}")
async def transformCrs(data_id, epsg):
    path = './data/' + data_id + '.geojson'
    before_epsg = e.getEpsg(data_id)
    r = tc.transform(path, before_epsg, epsg)
    return r

@app.get("/getTestPaths/")
async def getTestPaths():
	li = gp.getTestPaths()
	return li

@app.get("/getTestPeopleCount/")
async def getTestPeopleCount():
	return gpc.getTestPeopleCount("data/shibuya-scranble.jpg")

@app.get("/getTestNearest/")
async def getTestNearest():
	return gn.get_nearest_data(2, [136.59296264011894, 36.446592330984636])
