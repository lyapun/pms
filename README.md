# PMS - Property Management System

## Installation

1. First pull docker image:

```
docker pull lyapun/pms
```

2. Then you need to execute migrations to create database:

```
docker run -v <path to folder where you want to have db>:/app/db lyapun/pms python manage.py migrate --noinput
```

3. Then you can create user for you to use:

```
docker run -it -v <path to folder where you want to have db>:/app/db lyapun/pms python manage.py createsuperuser  
```

4. Finally you can execute container as web application:

```
docker run -p 127.0.0.1:8000:8000 -v <path to folder where you want to have db>:/app/db lyapun/pms
```

## Usage

1. Go to http://localhost:8000/api-auth/login/ to sign in
2. Then you can go to http://localhost:8000/api/v1/reservations/ to explore API.

## Tests

If you want to execute tests, you need to install project locally, because container doesn't have dev dependencies.

To do it, execute:

```
pip install -r requirements-dev.txt
```

And then you can execute tests:

```
make test
```


