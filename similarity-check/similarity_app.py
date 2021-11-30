import os
import io
import pickle
import uvicorn
import numpy as np
from fastapi import FastAPI, UploadFile, File, Request
from feature_vectors_model import FeatureExtraction
from torchvision import transforms
from PIL import Image
from starlette.responses import Response
import boto3
import json

app = FastAPI()

s3 = boto3.resource('s3')
vectors = pickle.loads(s3.Bucket("images-from-web").Object("test_vectors.pkl").get()['Body'].read())
names = pickle.loads(s3.Bucket("images-from-web").Object("test_names.pkl").get()['Body'].read())
    
with open("./similarity_model.pickle", "rb") as m:
    similarity_model = pickle.load(m)


feature_extraction = FeatureExtraction("avgpool")
feature_extraction.eval()
transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((256, 256))
    ])


def transform_to_vec(img):
    image = transform(img)
    vec = feature_extraction(image.unsqueeze(0))
    vec = vec.squeeze(-1).squeeze(-1).detach().numpy()
    return vec


@app.get('/')
async def root():
    return "Use post method using /predict or get method with /docs"


@app.post('/predict')
async def prediction(file: UploadFile = File(...)):
    raw_file = file.file.read()
    raw_file = Image.open(io.BytesIO(raw_file))
    transformed_img = transform_to_vec(raw_file)
    distance, index = similarity_model.kneighbors(transformed_img.reshape(1, -1))
    result = []
    for i in range(distance[0].shape[0]):
        result.append(names[index[0][i]])
    return {'result': result}


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
