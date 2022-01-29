from typing import List
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
# import io, pandas
import json

from strage_info.get_data_info import get_data_info
from response_manager import create_response

app = FastAPI()

@app.get("/")
async def root():
    response = {"message": "Hello World"}
    return response

@app.get("/0/data/")
async def get_data(process: List[str]=Query(None)):
    response = create_response(process)
    return response
