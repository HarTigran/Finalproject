[![Scraping Craigslist](https://github.com/HarTigran/Finalproject/actions/workflows/main.yml/badge.svg)](https://github.com/HarTigran/Finalproject/actions/workflows/main.yml)

# Finalproject

## Description of application

A similar car finder app searches for similar cars in Craigslist posts (several major cities) and returns car photos and prices listed on Craigslist.

### How it works

- Upload the image on the following [web page.](http://car-project-alb-843682670.us-east-1.elb.amazonaws.com/)
- Press "**Similar Cars**"
- The app will return the 5 most similar cars currently available on Craigslist with its price.

### Services and Applications Used

_Data collection_

1. **Github Action** to run Scrapy and push collected data to AWS S3 (post information and pictures's URLs)
2. **Scrapy** to crawl Craigslist
3. **AWS S3** to store collected data
4. **AWS Lambda** triggered by an event when GitHub pushes data to S3
5. **AWS SQS** to send URLs to AWS Lambda to download images to S3

_Main Process_

6. **Docker** to dockerize frontend:Stramlit and backend:FastApi with pre trained machine learning models
7. **AWS Elastic Container Registry** to store dockers
8. **AWS Elastic Container Services** to orchestrate container with two dockers
9. **AWS Fargate** to run AWS Elastic Container Services
10. **Stramlit** as User Interface to pass the request to FastAPI application and request images and price from S3, once FastAPI responds 
11. **FastAPI** to receive a request from streamlit find similar vehicles and send a response to streamlit

### Model

The main stage of similarity checking is performed by comparing the distance of the vector of the loaded car image with the vectors of the car images obtained from Craigslist.
Vector transformation logic is built by cutting last layer machine learning process.

## Architecture

![Diagram](https://github.com/HarTigran/Finalproject/blob/main/car-project-master/Images/Car-project-Draw.png?raw=true)

