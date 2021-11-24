import requests
import streamlit as st
from PIL import Image
from itertools import cycle
import boto3
from PIL import Image
from io import BytesIO
import numpy as np

st.sidebar.button("Sidebar button")
st.header("This is our APP!")


#test_image = Image.open("C:\\Users\\harut\\OneDrive\\Pictures\\Octocat.png").resize((225, 325), Image.ANTIALIAS)
#test_image2 = Image.open("C:\\Users\\harut\\OneDrive\\Pictures\\OTgxd3mt.jpg").resize((225, 325), Image.ANTIALIAS)

# st.image(test_image, caption='3000$')
# st.image(test_image2, caption='2300$')


def load_image(image_file):
	img = Image.open(image_file)
	return img



#st.subheader("Image")
image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])

if image_file is not None:

    # To See details
    st.write("The image you have uploaded:")
    #st.write(image_file.name)

    # To View Uploaded Image
    st.image(load_image(image_file), width=250)
    st.write("")
    st.write("")
    st.header("Similar cars are:")

s3 = boto3.resource('s3')
bucket = s3.Bucket('images-from-web')
# Iterates through all the objects, doing the pagination for you. Each obj
# is an ObjectSummary, so it doesn't contain the body. You'll need to call
# get to get the whole body.
object = bucket.Object('image_00V0V_13dmQl32leAz_0CI0t2.jpeg')
response = object.get()
file_stream = response['Body']
im = Image.open(file_stream)

filteredImages = [im] # your images here
caption = ["2332"] # your caption here
cols = cycle(st.columns(1)) # st.columns here since it is out of beta at the time I'm writing this
for idx, filteredImage in enumerate(filteredImages):
    next(cols).image(filteredImage, width=150, caption=caption[idx])