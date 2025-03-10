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
- **Methods**: GET, POST, PUT, DELETE

## Students

- **Endpoint**: `/students/`
- **Description**: Student management endpoints.
- **Methods**: GET, POST, PUT, DELETE

## Teachers

- **Endpoint**: `/teachers/`
- **Description**: Teacher management endpoints.
- **Methods**: GET, POST, PUT, DELETE

## Subjects

- **Endpoint**: `/subjects/`
- **Description**: Subject management endpoints.
- **Methods**: GET, POST, PUT, DELETE

## Attendance

- **Endpoint**: `/attendance/`
- **Description**: Attendance management endpoints.
- **Methods**: GET, POST, PUT, DELETE

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
