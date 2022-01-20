from typing import List
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
# import io, pandas
import json

from strage_info.get_data_info import get_data_info
from response_manager import create_response, create_response_with_processing

app = FastAPI()

@app.get("/")
async def root():
    response = {"message": "Hello World"}
    return response

@app.get("/data/{data_name}/")
async def getData(data_name, spatial_range: str=None, time_range: str=None, attribute: str=None):
    response = create_response(data_name, spatial_range, time_range, attribute, None)
    return response

@app.get("/processed_data/") # pm.ProcessingModel
async def get_processed_data(spatial_range: str=None, time_range: str=None, attribute: str=None, data_creation_process: List[str]=Query(None)):
    response = create_response_with_processing(data_creation_process, spatial_range, time_range, attribute)
    return response
