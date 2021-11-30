import os
import io
import uvicorn
import numpy as np
from fastapi import FastAPI, UploadFile, File, Request
from PIL import Image
from starlette.responses import Response
import boto3
import json

app = FastAPI()


@app.get('/')
async def root():
    return "Use post method using /predict or get method with /docs"



# async def prediction(img: UploadFile = File(...)):
#     raw_file = img.file.read()
#     raw_file = Image.open(io.BytesIO(raw_file))
#     result = ['helo-helo']
#     return Response('Hello, world!', media_type='text/plain')
@app.post('/predict')    
def get_image(file: UploadFile = File(...)):
    raw_file = file.file.read()
    raw_file = Image.open(io.BytesIO(raw_file))
    print(np.array(raw_file).shape)
    name = [np.array(raw_file).shape]
    return {"item": name}


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
