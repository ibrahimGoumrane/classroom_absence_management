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
cd classroom-absence-management/backend
```

### 2. Set Up Environment Variables
Create a .env file in the root of the backend directory. This file will store your sensitive information such as database credentials.

### Example .env file:
```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db  # 'db' for Docker container name
DB_PORT=3306
```
## 3 . Install Python Dependencies

pip install -r requirements.txt

## Alterantive Solution using Docker 

The project is containerized using Docker. To build and start the application, you will use **Make** along with Docker Compose.

### 1. Install Make
Make sure Make is installed on your system. If you don't have it installed, follow the instructions below based on your operating system:

If you're using WSL (Windows Subsystem for Linux), install make as follows: (The one used to install docker in ur machine )

U can access the lunix terminal on vscode : 
click on the  small arrow next to powershell in the terminal than git bash and there run :

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

