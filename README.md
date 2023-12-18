# Medical Project API

## To start the app

1. Create a `.env` file with the following variables(ex. .env.example):

   - `POSTGRES_DB=`
   - `POSTGRES_USER=`
   - `POSTGRES_PASSWORD=`

2. Run the following command:

   docker-compose up

## Endpoints

- <http://127.0.0.1:8000/api/v1/images/> - [GET] Get images
- <http://127.0.0.1:8000/api/v1/images/> - [POST] Upload an image with or without annotations
- <http://127.0.0.1:8000/api/v1/annotations/> - [PUT] [PATCH] Update Annotations
- <http://127.0.0.1:8000/api/v1/annotations/internal> - [GET] Getting all annotations in internal format by photo ID 
- <http://127.0.0.1:8000/api/v1/annotations/external> - [GET] Getting all annotations in external format by photo ID
- <http://127.0.0.1:8000/swagger> - Swagger UI
- <http://127.0.0.1:8000/api-token-auth> - Generate token for user

## Default user credentials
      login: admin_user
      password: strong_password

## To run the tests

      docker-compose run --rm  api make test

## In case you need more test data you can run this command:
    
      docker-compose run --rm  api python manage.py populate_db {NUMBER OF VALUES}
