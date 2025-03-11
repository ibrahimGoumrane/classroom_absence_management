# Backend: Classroom Absence Management System

This is the backend part of the **Classroom Absence Management System**, built with Django and MySQL. The backend is responsible for processing attendance data, handling user management, and interacting with the MySQL database. It also includes image recognition and manages attendance records based on student images.

## Features

- **Attendance Tracking**: Process student images and mark attendance.
- **User Management**: Manage students, teachers, and other users.
- **Database Integration**: MySQL is used to store user, attendance, and other records.
- **Django API**: Exposes API endpoints for the frontend and admin interface.
- **Dockerized**: The backend is containerized using Docker for easy deployment and scalability.

## Prerequisites

Before getting started, ensure you have the following installed:

- Python 3.x
- Docker
- Docker Compose
- MySQL 5.7 (handled by Docker)

## Getting Started

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/classroom-absence-management.git
cd classroom-absence-management
```

## 2 . Install Python Dependencies

pip install -r requirements.txt

### 3. Set Up Environment Variables

Create a file named .env in the same directory as example.env, using the structure provided in example.env as a template. Populate it with your sensitive information, such as database credentials, to securely store these details for your application.

### Generate a Django secret key:

Using Django's built-in utility in terminal:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## Alterantive Solution using Docker

The project is containerized using Docker. To build and start the application, you will use **Make** along with Docker Compose.

### 1. Install Make

Make sure Make is installed on your system. If you don't have it installed, follow the instructions below based on your operating system:

If you're using WSL (Windows Subsystem for Linux), install make as follows: (The one used to install docker in ur machine )

U can access the lunix terminal on vscode :
click on the small arrow next to powershell in the terminal than git bash and there run :

```bash
sudo apt update
sudo apt install make
```

## 2. Start the Containers

Once Make is installed, you can easily manage the Docker containers using the Makefile included in this project. To bring up the Docker containers (build and start them), simply run:

```bash
make up
```

See the makefile that contain different command to manage ur web service and migrations .

# API Endpoints Documentation

## Users

- **Endpoint**: `/users/`
- **Description**: User management endpoints.
- **Methods**: GET, POST, PATCH, DELETE

## Students

- **Endpoint**: `/students/`
- **Description**: Student management endpoints.
- **Methods**: GET, POST, PATCH, DELETE

## Teachers

- **Endpoint**: `/teachers/`
- **Description**: Teacher management endpoints.
- **Methods**: GET, POST, PATCH, DELETE

## Subjects

- **Endpoint**: `/subjects/`
- **Description**: Subject management endpoints.
- **Methods**: GET, POST, PATCH, DELETE

## Attendance

- **Endpoint**: `/attendance/`
- **Description**: Attendance management endpoints.
- **Methods**: GET, POST, PATCH, DELETE

## Admin

- **Endpoint**: `/admin/`
- **Description**: Django admin interface.
- **Methods**: GET

### API Usage Examples

### GET Request

```sh
curl -X GET http://localhost:8000/users/
```

### POST Request

```sh
curl -X POST http://localhost:8000/users/ -H "Content-Type: application/json" -d '{"KEY":"VALUE"}'
```

### PATCH Request

```sh
curl -X PATCH http://localhost:8000/users/1/ -H "Content-Type: application/json" -d '{"KEY":"VALUE"}'
```

### DELETE Request

```sh
curl -X DELETE http://localhost:8000/users/1/
```


## API documentation :

### Authentication EndPoints :

### CSRF Token Usage  

#### What is CSRF?  
CSRF (Cross-Site Request Forgery) protects against unauthorized requests on behalf of users.  

#### How to Retrieve CSRF Token?  
1. Make a **GET request** to `/api/login` or `/api/signup`.  
2. Check response **cookies** for `csrftoken`.  

#### How to Send CSRF Token?  
Include in **headers** for POST, PUT, PATCH, DELETE:  

```http
X-CSRFToken: <your_csrf_token>
```

### Signup

**Endpoint**: `/api/signup/`

**Method**: `POST`

**Description**: Create a new user account. This endpoint is used to register new users.

**Request Headers**:
- `Content-Type: application/json`

**Request Body**:
```json
{
    "email": "student@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "password": "securepassword123"
}
```

### Login

**Endpoint**: `/api/login/`

**Method**: `POST`

**Description**: Authenticate a user and start a session. This endpoint is used for user login.

**Request Headers**:
- `Content-Type: application/json`

**Request Body**:
```json
{
    "email": "student@example.com",
    "password": "securepassword123"
}
```


### Logout

**Endpoint**: `/api/logout/`

**Method**: `POST`

**Description**: Log out the user and end the session. This endpoint is used to log out the user.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`



Sure! Here is a section you can add to your README file about the Users API, including endpoints and examples of usage:

## Users Endpoints

### Overview

The Users API provides endpoints for managing user accounts. Only admins and the user who owns the account can update or delete the user. Admins have full access to all user management actions.


### List Users

**Endpoint**: `/api/users/`

**Method**: `GET`

**Description**: Retrieve a list of all users.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`


### Retrieve User

**Endpoint**: `/api/users/{id}/`

**Method**: `GET`

**Description**: Retrieve details of a specific user by ID.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

### Create User

**Endpoint**: `/api/users/`

**Method**: `POST`

**Description**: Create a new user account.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

**Request Body**:
```json
{
    "email": "newuser@example.com",
    "firstName": "UpdatedFirstName",
    "lastName": "UpdatedLastName",
    "password": "securepassword123",
    "role": "student"
}
```

### Update User

**Endpoint**: `/api/users/{id}/`

**Method**: `PATCH`

**Description**: Update details of a specific user by ID. Only the user who owns the account or an admin can update the user.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

**Request Body**:
```json
{
    "firstName": "UpdatedFirstName",
    "lastName": "UpdatedLastName"
}
```


### Delete User

**Endpoint**: `/api/users/{id}/`

**Method**: `DELETE`

**Description**: Delete a specific user by ID. Only the user who owns the account or an admin can delete the user.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`



