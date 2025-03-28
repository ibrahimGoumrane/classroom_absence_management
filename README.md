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
1. Make  a**GET request**  `/api/login` or `/api/signup`.  
2. Check response **cookies** for `csrftoken`.  

#### How to Send CSRF Token?  
Include in **headers** for POST, PUT, PATCH, DELETE:  

```http
X-CSRFToken: <your_csrf_token>
```
### Get Logged In user  
**Endpoint**: `/api/user/`

**Method**: `GET`

**Description**: Check Logged In user.

**Request Headers**:
- `Content-Type: application/json`





### Signup

**Endpoint**: `/api/signup/`

**Method**: `POST`

**Description**: Create a new user account. This endpoint is used to register new users.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`


**Request Body**:
```json
{ 
    "user" : {
        "email": "student@example.com",
        "firstName": "John",
        "lastName": "Doe",
        "password": "securepassword123"
    } , 
    "section_promo": 1
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


## Teachers API Endpoints

### Overview

The Teachers API provides endpoints for managing teacher accounts. Only admins and the teacher who owns the account can update or delete the teacher. Admins have full access to all teacher management actions.

### List Teachers

**Endpoint**: `/api/teachers/`

**Method**: `GET`

**Description**: Retrieve a list of all teachers.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

### Retrieve Teacher

**Endpoint**: `/api/teachers/{id}/`

**Method**: `GET`

**Description**: Retrieve details of a specific teacher by ID.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

### Create Teacher

**Endpoint**: `/api/teachers/`

**Method**: `POST`

**Description**: Create a new teacher account. Only admins can create new teachers.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

**Request Body**:
```json
{
    "user":{
    "email": "student18@example.com",
    "firstName": "John2",
    "lastName": "Doe2",
    "password": "securepassword123"
    } ,
    "department":"Meca"
}
```


### Update Teacher

**Endpoint**: `/api/teachers/{id}/`

**Method**: `PATCH`

**Description**: Update details of a specific teacher by ID. Only the teacher who owns the account or an admin can update the teacher.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

**Request Body**:
```json
{
    "user":{
    "email": "student18@example.com",
    "firstName": "John2",
    "lastName": "Doe2",
    "password": "securepassword123"
    } ,
    "department":"Meca"
}
```

### Delete Teacher

**Endpoint**: `/api/teachers/{id}/`

**Method**: `DELETE`

**Description**: Delete a specific teacher by ID. Only the teacher who owns the account or an admin can delete the teacher.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`


## Subjects API Endpoints

### Overview

The Subjects API provides endpoints for managing subjects. Only authenticated teachers can create or update subjects, and the teacher assigned to a subject is the one who is logged in. Admins have full access to all subject management actions.

### List Subjects

**Endpoint**: `/api/subjects/`

**Method**: `GET`

**Description**: Retrieve a list of all subjects.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`


### Retrieve Subject

**Endpoint**: `/api/subjects/{id}/`

**Method**: `GET`

**Description**: Retrieve details of a specific subject by ID.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`



### Create Subject

**Endpoint**: `/api/subjects/`

**Method**: `POST`

**Description**: Create a new subject. Only authenticated teachers can create subjects, and the teacher assigned to the subject is the one who is logged in.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

**Request Body**:
```json
{
    "name": "Mathematics"
}
```



### Update Subject

**Endpoint**: `/api/subjects/{id}/`

**Method**: `PATCH`

**Description**: Update details of a specific subject by ID. Only the teacher who owns the subject or an admin can update the subject.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

**Request Body**:
```json
{
    "name": "Advanced Mathematics"
}
```


### Delete Subject

**Endpoint**: `/api/subjects/{id}/`

**Method**: `DELETE`

**Description**: Delete a specific subject by ID. Only the teacher who owns the subject or an admin can delete the subject.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`



## Classes API Endpoints

### Overview

The Classes API provides endpoints for managing classes. Only authenticated users with admin permissions can create, update, or delete classes. Anyone can view the list of classes or retrieve details of a specific class.

### List Classes

**Endpoint**: `/api/classes/`

**Method**: `GET`

**Description**: Retrieve a list of all classes.

**Request Headers**:
- `Content-Type: application/json`

### Retrieve Class

**Endpoint**: `/api/classes/{id}/`

**Method**: `GET`

**Description**: Retrieve details of a specific class by ID.

**Request Headers**:
- `Content-Type: application/json`

### Create Class

**Endpoint**: `/api/classes/`

**Method**: `POST`

**Description**: Create a new class. Only authenticated users with admin permissions can create classes.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

**Request Body**:
```json
{
    "name": "Class A"
}
```

### Update Class

**Endpoint**: `/api/classes/{id}/`

**Method**: `PATCH`

**Description**: Update details of a specific class by ID. Only authenticated users with admin permissions can update classes.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

**Request Body**:
```json
{
    "name": "Updated Class A"
}
```

### Delete Class

**Endpoint**: `/api/classes/{id}/`

**Method**: `DELETE`

**Description**: Delete a specific class by ID. Only authenticated users with admin permissions can delete classes.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

## Students API Endpoints

### Overview

The Students API provides endpoints for managing student accounts. Only authenticated users with admin permissions can create, update, or delete students. Anyone can view the list of students or retrieve details of a specific student.

### List Students

**Endpoint**: `/api/students/`

**Method**: `GET`

**Description**: Retrieve a list of all students.

**Request Headers**:
- `Content-Type: application/json`

### Retrieve Student

**Endpoint**: `/api/students/{id}/`

**Method**: `GET`

**Description**: Retrieve details of a specific student by ID.

**Request Headers**:
- `Content-Type: application/json`

### Create Student

**Endpoint**: `/api/students/`

**Method**: `POST`

**Description**: Create a new student account. Only authenticated users with admin permissions can create students.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

**Request Body**:
```json
{
    "user": {
        "email": "newstudent@example.com",
        "firstName": "New",
        "lastName": "Student",
        "password": "securepassword123"
    },
    "section_promo": 1,
}
```

### Update Student

**Endpoint**: `/api/students/{id}/`

**Method**: `PATCH`

**Description**: Update details of a specific student by ID. Only the student who owns the account or an admin can update the student.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

**Request Body**:
```json
{
    "user": {
        "email": "updated.email@example.com",
        "firstName": "UpdatedFirstName",
        "lastName": "UpdatedLastName"
    },
    "section_promo": 2,
}
```

### Delete Student

**Endpoint**: `/api/students/{id}/`

**Method**: `DELETE`

**Description**: Delete a specific student by ID. Only the student who owns the account or an admin can delete the student.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

## Attendance API Endpoints

### Overview

The Attendance API provides endpoints for managing attendance records. Only authenticated users with teacher or admin permissions can create, update, or delete attendance records. Anyone can view the list of attendance records or retrieve details of a specific attendance record.

### List Attendance Records

**Endpoint**: `/api/attendance/`

**Method**: `GET`

**Description**: Retrieve a list of all attendance records.

**Request Headers**:
- `Content-Type: application/json`

**Example Using `curl`**:
```sh
curl -X GET http://localhost:8000/api/attendance/ \
-H "Content-Type: application/json"
```

### Retrieve Attendance Record

**Endpoint**: `/api/attendance/{id}/`

**Method**: `GET`

**Description**: Retrieve details of a specific attendance record by ID.

**Request Headers**:
- `Content-Type: application/json`


### Create Attendance Record

**Endpoint**: `/api/attendance/`

**Method**: `POST`

**Description**: Create a new attendance record. Only authenticated users with teacher or admin permissions can create attendance records.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

**Request Body**:
```json
{
    "student": 1,
    "date": "2025-03-12",
    "status": "present"
}
```


### Update Attendance Record

**Endpoint**: `/api/attendance/{id}/`

**Method**: `PATCH`

**Description**: Update details of a specific attendance record by ID. Only authenticated users with teacher or admin permissions can update attendance records.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

**Request Body**:
```json
{
    "status": "absent"
}
```


### Delete Attendance Record

**Endpoint**: `/api/attendance/{id}/`

**Method**: `DELETE`

**Description**: Delete a specific attendance record by ID. Only authenticated users with teacher or admin permissions can delete attendance records.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

## Student Images API Endpoints

### Overview

The Student Images API provides endpoints for managing student images. Only authenticated users with admin permissions can create, update, or delete student images. Anyone can view the list of student images or retrieve details of a specific student image.

### List Student Images

**Endpoint**: `/api/studentimages/?student=<id>`

**Method**: `GET`

**Description**: Retrieve a list of all student images with that id if ur are admin , but if u are a student get all ur images .

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

### Retrieve Student Image

**Endpoint**: `/api/studentimages/{id}/`

**Method**: `GET`

**Description**: Retrieve details of a specific student image by ID.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

### Create Student Image

**Endpoint**: `/api/studentimages/`

**Method**: `POST`

**Description**: Create a new student image. Only authenticated users with admin permissions can create student images.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

**Request Body**:
```json
{
    "student": 1,
    "image": "base64_encoded_image_data"
}
```


### Delete Student Image

**Endpoint**: `/api/studentimages/{id}/`

**Method**: `DELETE`

**Description**: Delete a specific student image by ID. Only authenticated users with admin permissions can delete student images.

**Request Headers**:
- `Content-Type: application/json`
- `Cookie: sessionid=<your_session_id>`
- `Headers: X-CSRFToken=<your_token>`

