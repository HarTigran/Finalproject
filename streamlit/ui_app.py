import requests
import streamlit as st
from PIL import Image
from itertools import cycle
import boto3
import numpy as np
from requests_toolbelt.multipart.encoder import MultipartEncoder
import csv
import pandas as pd

# Interact with FastAPI endpoint
url = 'http://localhost:8080'
endpoint = '/predict'
    
# construct UI layout

st.sidebar.button("Sidebar button")
st.header("This is our APP!")


s3 = boto3.client('s3')

#fetch the file from s3
response = s3.get_object(Bucket = 'images-from-web', Key = 'test.csv')
        
# deserialize the file's content
        
lines = response['Body'].read().decode('utf-8').splitlines(True)

reader = csv.DictReader(lines)
df = pd.DataFrame(reader)
# upload image
image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
# connect to s3
s3 = boto3.resource('s3')
bucket = s3.Bucket('images-from-web')

if st.button('Get Similar Cars'):
    if image_file is None:
        st.write('Insert an Image')
    else:
        st.write('Your Image')
        st.image(image_file)
        files = {"file": image_file.getvalue()}
        res = requests.post('http://localhost:8080/predict', files=files)
        img_lst = res.json()
        
        st.write('Similar Results')
        for image in img_lst["result"]:
            object = bucket.Object(image.split('/')[-1])
            response = object.get()
            file_stream = response['Body']
            im = Image.open(file_stream)
            filteredImages = [im] # your images here
            info = df[df.iloc[:,2].str.contains(image.split('/')[-1].split('.')[0])][:1]
            caption = [info['car_price'].iloc[0]]  # your caption here 
            cols = cycle(st.columns(1)) # st.columns here since it is out of beta at the time I'm writing this
            for idx, filteredImage in enumerate(filteredImages):
                next(cols).image(filteredImage, width=300, caption=caption[idx])
        
        

