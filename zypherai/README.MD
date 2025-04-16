This assessment implements a Flask-based machine learning prediction API with both synchronous and asynchronous support. 
Assynchronous predictions are processed using custom queue built with Redis and a background worker thread. 

Below are the features that I have implemented in the assessment according to the instructions given to me:

- Sync & Async prediction via /predict endpoint

- Redis-powered queue for async tasks

- Background thread to consume and process tasks

-  Result retrieval via /predict/prediction_id endpoint

- Docker + Docker Compose ready

Step by step on how to run this assessment:

My files are organized as follows:

- One main folder called zypherai
- This folder has 5 files called app.py(which contains the python code for async and sync predictions via endpoint)
- It also has requirements.txt which has all the python dependencies
- It has Dockerfile which will build the docker image for the flask app. 
- It also has docker-compose.yml 
- Finally a Readme file - the file which you are reading right now which contains my approach and how to run this file. 

To run this file

- docker-compose up --build

Thats it! Now you can see and test this. 

Moreover for testing if my post and get end-points are working properly, i have tested it with postman desktop app, and it was working fine. Tested it on postman with a couple of testcases. 

A bit about my approach:

This Flask-based web application provides both synchronous and asynchronous prediction services using a Redis-backed queue system. When a user submits a prediction request, the app either processes it immediately (sync) or queues it for background processing (async) based on the request header. Asynchronous requests are pushed into a Redis list, and a background worker thread continuously polls this queue to simulate processing, update the status in Redis, and store the result. Clients can then retrieve the result using a unique prediction ID.

