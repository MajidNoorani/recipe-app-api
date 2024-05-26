# recipe-app-api
This is a Recipe API Project developed on the Django REST framework which is a backend for a webapp that each user would be able to add his/her food recipes with related tags and images.

Each recipe contains this information:
1- Title
2- Description
3- Estimated Time
4- Ingredients
5- Price
6- Related Link
7- Image

The recipes are searchable with Tags and Ingredients. Also, the user credentials are done using Email and Password and also OAuth token is used.

## Run The Project
The project is dockerized and a [docker-compose.yml](docker-compose.yml) file is added to project. So, after building the container using 
```
docker compose build .
```
you need to migrate the database:
```
docker compose run --rm app sh -c "python manage.py makemigrations"
docker compose run --rm app sh -c "python manage.py migrate"
```
you can run the project with this code:
```
docker compose up
```

if you do not want to use docker container you just need to install the [requirements](requirements.txt) and then run:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runsrver
```

## Super User Creation
#### Docker based:
```
docker compose run --rm app sh -c "python manage.py createsuperuser"
```
#### Without docker:
```
python manage.py createsuperuser
```

## About The Project
There is a [wait_for_db.py](/app/core/management/commands/wait_for_db.py) file which checks the health of the connection to the database. If you are running the code using docker, it will automatically run this file first and if there is no problem with the connection to the database it will start the project.
Also, the development is done on a Test Driven Development approach and by pushing the codes since I have configured a GitHub action it will automatically test the codes and it also does the linting checks. you can test the codes manally using this code:
```
docker compose run --rm app sh -c "python manage.py test && flake8"
```








