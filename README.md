# Events Management API

A Django REST framework API for managing events and user registrations, with Docker-based deployment and testing.

## Features

- User authentication (registration/login via tokens)
- Event CRUD operations
- Event registration management
- Swagger API documentation
- Dockerized development and testing environment

## Project Structure

Project is divided on 2 apps:

- Users - containing auth logic for users
- Events - containing event crud, and event registration
- Deploy - directory containing Docker related files

## Getting Started

To start project via docker:
- ```cd deploy/```
- ```docker-compose up --build --force-recreate --remove-oprphans api```
  
Or if you want to run tests in docker container you may:
- ```cd deploy/```
- ```docker-compose up --build --force-recreate --remove-oprphans tests```
  
To start locally:
- you need to create venv first
- ```python manage.py makemigrations```
- ```python manage.py migrate```
- ```python manage.py runserver```

For easier api testing experience i recommend accessing api via /swagger endpoint

### Prerequisites

- Docker 
- Docker Compose 
- Python 3.10+ (optional for local development)
