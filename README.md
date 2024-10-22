# Task Manager

This project implements a set of APIs for a task management app using Django &
Django Rest Framework that allows users to create tasks, assign tasks to users, and retrieve
tasks assigned to specific users.

Note: The project is functional in every condition except `task-manager` app cannot be built using the docker. Due to being busy with my other tasks as well as such short time line could not work on that.

Checkout Some other projects:
- [Image Processor](https://github.com/Confused-Tima/Image-Processor)
- [Data Aggregaor](https://github.com/Confused-Tima/Data-Aggregator)

## Project Setup

Install dependancies from requirements.txt file to create your env.

```bash
pip install -r requirements.txt
```

Either install `postgreSQL` or use the given docker compose file to run the postgres DB

```bash
docker compose up -d pg
```

In .env file use update the configs as per requirements:

```bash
# PostgresSQL Settings
PG_DB="task-manager"
PG_USER="postgres"
PG_PASS="1234"
PG_HOST="pg"
PG_PORT="5432"
```

Now apply the migrations:

```bash
python task_manager/manage.py makemigrations
python task_manager/manage.py migrate
```

Now run start the server:
Note: Will run in development mode only

```bash
python task_manager/manage.py runserver
```

Optionally create superuser for admin access:

```bash
python task_manager/manage.py createsuperser
```

## Description

This project handles:

- User creation
- Authentication using JWT
- Authorization (Only authorized users can create tasks, non-authorised users can only see tasks)
- Task creation
- Task assignment
- Assignee Removal
- User's Assigned tasks



## SignUp/LogIn User

First create user using `/api/users/signup/`

Request Format: 
- ```json
    {"username": "EXWHYZEE", "password": "123abc"}
    ```

Now login and fetch the refresh and access tokens.
Like the names suggest access token helps you access resources in the app where as refresh token helps to refresh access token when it expires.

These are Bearer token. So add the bearer keyword when sending request in headers. Header key: `Authorization`
In postman, go to Authorization, then select Bearer Token and add the complete token over there without bearer keyword.

In our app, everyone should be able to see the tasks but only authenticated users can change the resources.

I'm allowing all users to see is because I'm considering this project as an internal project which would only be accessible within an organisation and only those people should be able to see it. And for easier authorisation as well.

Use `api/users/token/refresh/` path to refresh tokens.
Use `api/users/login` when refresh token expires.

## Tasks

Tasks have many to many relationship with the users. So many users can work on the same task as well as a single user can also work on many tasks.

Django will maintain another table for this many to many relationship.

We are maintaining all the necesarry info regading the tasks, checkout at:
[Models](task_manager/tasks/models.py)


Checkout the Endpoints available at:
[Endpoints](task_manager/tasks/urls.py)

Checkout the code for the Enpoints at:
[Task Manager Code](task_manager/tasks/views.py)
