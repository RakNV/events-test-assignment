# Events Management API

A Django REST framework API for managing events and user registrations, with Docker-based deployment and testing.

## Features

- User authentication (registration/login via tokens)
- Event CRUD operations
- Event registration management
- Swagger API documentation
- Dockerized development and testing environment

## Project Structure

Project main logic is contained in 4 directories:

- users/ - containing auth logic for users
- events/ - containing event crud, and event registration
- deploy/ - directory containing Docker related files
- events_project/ - django project settings

## Getting Started

To start project via docker:
- ```cd deploy/```
- ```docker-compose up --build --force-recreate --remove-oprphans api```
  
Or if you want to run tests in docker container you may:
- ```cd deploy/```
- ```docker-compose up --build --force-recreate --remove-oprphans tests```
  
To start locally:
- you need to create venv first, for example ```python3 -m venv venv```
- activate venv ```. ./venv/bin/activate```
- run ```pip install -r requirements.txt``` to install dependencies
- ```python manage.py makemigrations```
- ```python manage.py migrate```
- ```python manage.py runserver```

For easier api testing experience i recommend accessing api via /swagger endpoint

### Prerequisites

- Docker 
- Docker Compose 
- Python 3.10+ (optional for local development)
