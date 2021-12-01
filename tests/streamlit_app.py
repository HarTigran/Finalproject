import requests
import json
import streamlit as st
from PIL import Image
from itertools import cycle
import boto3
import numpy as np
from requests_toolbelt.multipart.encoder import MultipartEncoder

#Interact with FastAPI endpoint
url = 'http://0.0.0.0:8080'
endpoint = '/predict'

# def process(image, server_url: str):
#     m = MultipartEncoder(
#         fields = {'file': ('filename', image, 'image/jpeg')}
#         )
        
#     r = requests.post(server_url,
#                     data = m,
#                     headers = {'Content-Type': m.content_type},
#                     timeout = 8080)
    
#    return r
    
# construct UI layout

st.sidebar.button("Sidebar button")
st.header("This is our APP!")


#test_image = Image.open("C:\\Users\\harut\\OneDrive\\Pictures\\Octocat.png").resize((225, 325), Image.ANTIALIAS)
#test_image2 = Image.open("C:\\Users\\harut\\OneDrive\\Pictures\\OTgxd3mt.jpg").resize((225, 325), Image.ANTIALIAS)

# st.image(test_image, caption='3000$')
# st.image(test_image2, caption='2300$')


# def load_image(image_file):
# 	img = Image.open(image_file)
# 	return img



# upload image
image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])

# connect to s3
s3 = boto3.resource('s3')
bucket = s3.Bucket('images-from-web')

if st.button('Get Similar Cars'):
    if image_file is None:
        st.write('Insert an Image')
    else:
        files = {"file": image_file.getvalue()}
        img_lst = requests.post("http://0.0.0.0:8080/predict", files=files)
        img_url = img_lst.json()
        st.write(img_url)
       
        for image in img_url["item"]:
            st.write(image)
            object = bucket.Object(image.split('/')[-1])
            response = object.get()
            file_stream = response['Body']
            im = Image.open(file_stream)
            filteredImages = [im] # your images here
            caption = ["2332"] # your caption here
            cols = cycle(st.columns(1)) # st.columns here since it is out of beta at the time I'm writing this
            for idx, filteredImage in enumerate(filteredImages):
                next(cols).image(filteredImage, width=150, caption=caption[idx])
        
        
        
    # To View Uploaded Image
    # st.image(load_image(image_file), width=250)
    # st.write("")
    # st.write("")
    # st.header("Similar cars are:")


# Iterates through all the objects, doing the pagination for you. Each obj
# is an ObjectSummary, so it doesn't contain the body. You'll need to call
# get to get the whole body.


