# Backend: Classroom Absence Management System

This is the backend component of the **Classroom Absence Management System**, built with Django and MySQL. It's responsible for handling attendance data, user management, and interacting with the MySQL database. The backend also includes image recognition capabilities for managing attendance records based on student images.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Install Python Dependencies (if not using Docker)](#2-install-python-dependencies-if-not-using-docker)
  - [3. Set Up Environment Variables](#3-set-up-environment-variables)
  - [4. Generate a Django Secret Key](#4-generate-a-django-secret-key)
- [Alternative Solution: Using Docker](#alternative-solution-using-docker)
  - [1. Install Make (if necessary)](#1-install-make-if-necessary)
  - [2. Start the Containers](#2-start-the-containers)
- [API Endpoints Documentation](#api-endpoints-documentation)
  - [Authentication Endpoints](#authentication-endpoints)
    - [CSRF Token Usage](#csrf-token-usage)
    - [Get Logged-In User](#get-logged-in-user)
    - [Signup](#signup)
    - [Login](#login)
    - [Logout](#logout)
  - [Users Endpoints](#users-endpoints)
    - [Overview](#overview-1)
    - [List Users](#list-users)
    - [Retrieve User](#retrieve-user)
    - [Create User](#create-user)
    - [Update User](#update-user)
    - [Delete User](#delete-user)
  - [Departments API Endpoints](#departments-api-endpoints)
    - [Overview](#overview-2)
    - [List Departments](#list-departments)
    - [Retrieve Department](#retrieve-department)
    - [Create Department](#create-department)
    - [Update Department](#update-department)
    - [Delete Department](#delete-department)
  - [Teachers API Endpoints](#teachers-api-endpoints)
    - [Overview](#overview-2)
    - [List Teachers](#list-teachers)
    - [Retrieve Teacher](#retrieve-teacher)
    - [Create Teacher](#create-teacher)
    - [Update Teacher](#update-teacher)
    - [Delete Teacher](#delete-teacher)
  - [Subjects API Endpoints](#subjects-api-endpoints)
    - [Overview](#overview-3)
    - [List Subjects](#list-subjects)
    - [Retrieve Subject](#retrieve-subject)
    - [Create Subject](#create-subject)
    - [Update Subject](#update-subject)
    - [Delete Subject](#delete-subject)
  - [Classes API Endpoints](#classes-api-endpoints)
    - [Overview](#overview-4)
    - [List Classes](#list-classes)
    - [Retrieve Class](#retrieve-class)
    - [Create Class](#create-class)
    - [Update Class](#update-class)
    - [Delete Class](#delete-class)
  - [Students API Endpoints](#students-api-endpoints)
    - [Overview](#overview-5)
    - [List Students](#list-students)
    - [Retrieve Student](#retrieve-student)
    - [Create Student](#create-student)
    - [Update Student](#update-student)
    - [Delete Student](#delete-student)
  - [Attendance API Endpoints](#attendance-api-endpoints)
    - [Overview](#overview-6)
    - [List Attendance Records](#list-attendance-records)
    - [Retrieve Attendance Record](#retrieve-attendance-record)
    - [Create Attendance Record](#create-attendance-record)
    - [Update Attendance Record](#update-attendance-record)
    - [Delete Attendance Record](#delete-attendance-record)
    - [Generate Face Encodings](#generate-face-encodings)
    - [Process Attendance](#process-attendance)
    - [Confirm Attendance](#confirm-attendance)
  - [Student Images API Endpoints](#student-images-api-endpoints)
    - [Overview](#overview-7)
    - [List Student Images](#list-student-images)
    - [Retrieve Student Image](#retrieve-student-image)
    - [Create Student Image](#create-student-image)
    - [Delete Student Image](#delete-student-image)

## Features

- **Attendance Tracking:** Processes student images to automatically mark attendance.
- **User Management:** Manages student, teacher, and administrator accounts.
- **Database Integration:** Uses MySQL to store user data, attendance records, and other relevant information.
- **Django API:** Exposes REST API endpoints for use by the frontend and admin interface.
- **Dockerized:** Containerized using Docker for simplified deployment and scalability.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- Docker
- Docker Compose
- MySQL 5.7 (managed by Docker in the provided setup)

## Getting Started

### 1. Clone the Repository

Clone the project repository to your local machine:

```bash
git clone https://github.com/ibrahimGoumrane/classroom_absence_management.git
cd classroom_absence_management
```

### 2. Install Python Dependencies (if not using Docker)

If you're not using the Docker setup, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory, using `example.env` as a template. Populate the `.env` file with your sensitive information such as database credentials. This file should **not** be committed to version control.

### 4. Generate a Django Secret Key

Generate a unique secret key for your Django project:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copy the output of this command and paste it into your `.env` file.

## Alternative Solution: Using Docker

This project includes a Docker configuration for simplified setup and deployment.

### 1. Install Make (if necessary)

The provided `Makefile` simplifies common Docker Compose operations. If you don't have `make` installed:

**For Debian/Ubuntu (including WSL):**

```bash
sudo apt update
sudo apt install make
```

**Other operating systems:** Refer to your system's package manager or the official `make` documentation.

### 2. Start the Containers

Use the `Makefile` to build and start the Docker containers:

```bash
make up
```

This command will build the Docker image and start the containers defined in `docker-compose.yml`. Refer to the `Makefile` for other helpful commands (e.g., running migrations).

## API Endpoints Documentation

**Base URL:** `http://localhost:8000/api/` (or the appropriate address if running in a Docker container). All endpoints return JSON unless otherwise specified.

### Authentication Endpoints

#### CSRF Token Usage

CSRF (Cross-Site Request Forgery) protection is enabled.

- **Retrieving the CSRF Token:** Make a `GET` request to `/api/login/` or `/api/signup/`. The CSRF token will be in the `csrftoken` cookie of the response.
- **Sending the CSRF Token:** Include the CSRF token in the `X-CSRFToken` header for all `POST`, `PUT`, `PATCH`, and `DELETE` requests. Also include the `sessionid` cookie that u get once logged in .

Example header:

```http
X-CSRFToken: <your_csrf_token>
Cookie: sessionid=<your_session_id>
```

#### Get Logged-In User

- **Endpoint:** `/api/user/`
- **Method:** `GET`
- **Description:** Retrieves information about the currently logged-in user.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Get Logged-In Teacher

- **Endpoint:** `/api/user/teacher/`
- **Method:** `GET`
- **Description:** Retrieves information about the currently logged-in teacher.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Signup

- **Endpoint:** `/api/signup/`
- **Method:** `POST`
- **Description:** Creates a new user account.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "user": {
      "email": "student@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "password": "securepassword123"
    },
    "section_promo": 1
  }
  ```

#### Login

- **Endpoint:** `/api/login/`
- **Method:** `POST`
- **Description:** Authenticates a user and starts a session.
- **Request Headers:**
  - `Content-Type: application/json`
- **Request Body:**

  ```json
  {
    "email": "student@example.com",
    "password": "securepassword123"
  }
  ```

#### Logout

- **Endpoint:** `/api/logout/`
- **Method:** `POST`
- **Description:** Logs out the user and ends the session.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

### Users Endpoints

#### Overview

The Users API provides endpoints for managing user accounts. Admins have full access. Regular users can only update or delete their own accounts.

#### List Users

- **Endpoint:** `/api/users/`
- **Method:** `GET`
- **Description:** Retrieves a list of all users (Admin only).
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Retrieve User

- **Endpoint:** `/api/users/{id}/` (where `{id}` is the user ID)
- **Method:** `GET`
- **Description:** Retrieves details of a specific user.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Create User

- **Endpoint:** `/api/users/`
- **Method:** `POST`
- **Description:** Creates a new user account (Admin only).
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "email": "newuser@example.com",
    "firstName": "UpdatedFirstName",
    "lastName": "UpdatedLastName",
    "password": "securepassword123",
    "role": "student"
  }
  ```

#### Update User

- **Endpoint:** `/api/users/{id}/`
- **Method:** `PATCH`
- **Description:** Updates details of a specific user. Users can only update their own accounts; admins can update any account.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "firstName": "UpdatedFirstName",
    "lastName": "UpdatedLastName"
  }
  ```

#### Delete User

- **Endpoint:** `/api/users/{id}/`
- **Method:** `DELETE`
- **Description:** Deletes a specific user. Users can only delete their own accounts; admins can delete any account.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

### Departments API Endpoints

#### Overview

The Departments API provides endpoints for managing departments. Only authenticated users with admin permissions can create, update, or delete departments. Anyone can view the list of departments or retrieve details of a specific department.

#### List Departments

- **Endpoint:** `/api/departments/`
- **Method:** `GET`
- **Description:** Retrieves a list of all departments.
- **Request Headers:**
  - `Content-Type: application/json`

#### Retrieve Department

- **Endpoint:** `/api/departments/{id}/`
- **Method:** `GET`
- **Description:** Retrieves details of a specific department by ID.
- **Request Headers:**
  - `Content-Type: application/json`

#### Create Department

- **Endpoint:** `/api/departments/`
- **Method:** `POST`
- **Description:** Creates a new department. Only authenticated users with admin permissions can create departments.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "name": "Computer Science",
    "description": "The Department of Computer Science"
  }
  ```

#### Update Department

- **Endpoint:** `/api/departments/{id}/`
- **Method:** `PATCH`
- **Description:** Updates details of a specific department by ID. Only authenticated users with admin permissions can update departments.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "description": "The Department of Computer Science and Engineering"
  }
  ```

#### Delete Department

- **Endpoint:** `/api/departments/{id}/`
- **Method:** `DELETE`
- **Description:** Deletes a specific department by ID. Only authenticated users with admin permissions can delete departments.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

## Teachers API Endpoints

#### Overview

The Teachers API provides endpoints for managing teacher accounts and accessing teacher-related resources. Admins have full access. Regular teachers can only update or delete their own accounts.

#### List Teachers

- **Endpoint:** `/api/teachers/`
- **Method:** `GET`
- **Description:** Retrieves a list of all teachers.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Retrieve Teacher

- **Endpoint:** `/api/teachers/{id}/`
- **Method:** `GET`
- **Description:** Retrieves details of a specific teacher.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Create Teacher

- **Endpoint:** `/api/teachers/`
- **Method:** `POST`
- **Description:** Creates a new teacher account (Admin only).
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "user": {
      "email": "teacher1@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "password": "securepassword123"
    },
    "department": 1
  }
  ```

#### Update Teacher

- **Endpoint:** `/api/teachers/{id}/`
- **Method:** `PATCH`
- **Description:** Updates details of a specific teacher. Teachers can only update their own accounts; admins can update any account.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "user": {
      "firstName": "UpdatedFirstName",
      "lastName": "UpdatedLastName"
    },
    "department": 3
  }
  ```

#### Delete Teacher

- **Endpoint:** `/api/teachers/{id}/`
- **Method:** `DELETE`
- **Description:** Deletes a specific teacher. Teachers can only delete their own accounts; admins can delete any account.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Get Teacher Subjects

- **Endpoint:** `/api/teachers/{id}/subjects/`
- **Method:** `GET`
- **Description:** Retrieves all subjects taught by a specific teacher.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Response Example:**
  ```json
  [
    {
      "id": 1,
      "name": "Mathematics",
      "description": "Advanced mathematics course",
      "teacher": 1
    },
    {
      "id": 3,
      "name": "Physics",
      "description": "Introduction to physics",
      "teacher": 1
    }
  ]
  ```

#### Get Teacher Attendance Records

- **Endpoint:** `/api/teachers/{id}/attendance/`
- **Method:** `GET`
- **Description:** Retrieves all attendance records for subjects taught by a specific teacher.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Optional Query Parameters:**
  - `subject_id`: Filter by subject ID
  - `date_from`: Filter records on or after this date (YYYY-MM-DD)
  - `date_to`: Filter records on or before this date (YYYY-MM-DD)
- **Response Example:**
  ```json
  [
    {
      "id": 1,
      "student": 5,
      "subject": 2,
      "date": "2023-05-15",
      "status": "present",
      "student_details": {
        "id": 5,
        "name": "John Doe"
      },
      "subject_details": {
        "id": 2,
        "name": "Mathematics"
      }
    },
    {
      "id": 2,
      "student": 6,
      "subject": 2,
      "date": "2023-05-15",
      "status": "absent",
      "student_details": {
        "id": 6,
        "name": "Jane Smith"
      },
      "subject_details": {
        "id": 2,
        "name": "Mathematics"
      }
    }
  ]
  ```

### Subjects API Endpoints

#### Overview

The Subjects API provides endpoints for managing subjects. Only authenticated teachers can create or update subjects, and the teacher assigned to a subject is the one who is logged in. Admins have full access to all subject management actions.

#### List Subjects

- **Endpoint:** `/api/subjects/`
- **Method:** `GET`
- **Description:** Retrieves a list of all subjects.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Retrieve Subject

- **Endpoint:** `/api/subjects/{id}/`
- **Method:** `GET`
- **Description:** Retrieves details of a specific subject.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Create Subject

- **Endpoint:** `/api/subjects/`
- **Method:** `POST`
- **Description:** Creates a new subject. Only authenticated teachers can create subjects, and the teacher assigned to the subject is the one who is logged in.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "name": "Mathematics",
    "teacher": "1",
    "section_promo": "2"
  }
  ```

#### Update Subject

- **Endpoint:** `/api/subjects/{id}/`
- **Method:** `PATCH`
- **Description:** Updates details of a specific subject. Only the teacher who owns the subject or an admin can update the subject.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "name": "Advanced Mathematics",
    "teacher": "1",
    "section_promo": "2"
  }
  ```

#### Delete Subject

- **Endpoint:** `/api/subjects/{id}/`
- **Method:** `DELETE`
- **Description:** Deletes a specific subject. Only the teacher who owns the subject or an admin can delete the subject.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

### Classes API Endpoints

#### Overview

The Classes API provides endpoints for managing classes. Only authenticated users with admin permissions can create, update, or delete classes. Anyone can view the list of classes or retrieve details of a specific class.

#### List Classes

- **Endpoint:** `/api/classes/`
- **Method:** `GET`
- **Description:** Retrieves a list of all classes.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Retrieve Class

- **Endpoint:** `/api/classes/{id}/`
- **Method:** `GET`
- **Description:** Retrieves details of a specific class.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Create Class

- **Endpoint:** `/api/classes/`
- **Method:** `POST`
- **Description:** Creates a new class (Admin only).
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "name": "Class A"
  }
  ```

#### Update Class

- **Endpoint:** `/api/classes/{id}/`
- **Method:** `PATCH`
- **Description:** Updates details of a specific class (Admin only).
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "name": "Updated Class A"
  }
  ```

#### Delete Class

- **Endpoint:** `/api/classes/{id}/`
- **Method:** `DELETE`
- **Description:** Deletes a specific class (Admin only).
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

I'll add these class endpoints to the README documentation. They should be included in the Classes API Endpoints section.

Here's the documentation to add to your README:

````markdown
#### Get Class Students

- **Endpoint:** `/api/classes/{id}/students/`
- **Method:** `GET`
- **Description:** Retrieves all students belonging to a specific class.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Response Example:**
  ```json
  [
    {
      "id": 1,
      "user": {
        "id": 5,
        "email": "student1@example.com",
        "firstName": "John",
        "lastName": "Doe"
      },
      "section_promo": 1
    },
    {
      "id": 2,
      "user": {
        "id": 6,
        "email": "student2@example.com",
        "firstName": "Jane",
        "lastName": "Smith"
      },
      "section_promo": 1
    }
  ]
  ```
````

#### Get Class Attendance Records

- **Endpoint:** `/api/classes/{id}/attendance/`
- **Method:** `GET`
- **Description:** Retrieves all attendance records for students in a specific class.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Optional Query Parameters:**
  - `subject_id`: Filter by subject ID
  - `date_from`: Filter records on or after this date (YYYY-MM-DD)
  - `date_to`: Filter records on or before this date (YYYY-MM-DD)
- **Response Example:**
  ```json
  [
    {
      "id": 1,
      "student": 5,
      "subject": 2,
      "date": "2023-05-15",
      "status": "present",
      "student_details": {
        "id": 5,
        "firstName": "John",
        "lastName": "Doe"
      },
      "subject_details": {
        "id": 2,
        "name": "Mathematics"
      }
    },
    {
      "id": 2,
      "student": 6,
      "subject": 2,
      "date": "2023-05-15",
      "status": "absent",
      "student_details": {
        "id": 6,
        "firstName": "Jane",
        "lastName": "Smith"
      },
      "subject_details": {
        "id": 2,
        "name": "Mathematics"
      }
    }
  ]
  ```

#### Get Class Subjects

- **Endpoint:** `/api/classes/{id}/subjects/`
- **Method:** `GET`
- **Description:** Retrieves all subjects associated with a specific class.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Response Example:**
  ```json
  [
    {
      "id": 1,
      "name": "Mathematics",
      "description": "Advanced mathematics course",
      "teacher": {
        "id": 3,
        "user": {
          "id": 10,
          "firstName": "Robert",
          "lastName": "Johnson",
          "email": "robert.j@example.com"
        },
        "department": 1
      }
    },
    {
      "id": 2,
      "name": "Physics",
      "description": "Introduction to physics principles",
      "teacher": {
        "id": 4,
        "user": {
          "id": 11,
          "firstName": "Maria",
          "lastName": "Garcia",
          "email": "maria.g@example.com"
        },
        "department": 2
      }
    }
  ]
  ```

### Students API Endpoints

#### Overview

The Students API provides endpoints for managing student accounts. Only authenticated users with admin permissions can create, update, or delete students. Anyone can view the list of students or retrieve details of a specific student.

#### List Students

- **Endpoint:** `/api/students/`
- **Method:** `GET`
- **Description:** Retrieves a list of all students.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Retrieve Student

- **Endpoint:** `/api/students/{id}/`
- **Method:** `GET`
- **Description:** Retrieves details of a specific student.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Create Student

- **Endpoint:** `/api/students/`
- **Method:** `POST`
- **Description:** Creates a new student (Admin only).
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "user": {
      "email": "newstudent@example.com",
      "firstName": "New",
      "lastName": "Student",
      "password": "securepassword123"
    },
    "section_promo": 1
  }

#### Update Student

- **Endpoint:** `/api/students/{id}/`
- **Method:** `PATCH`
- **Description:** Updates details of a specific student. Students can only update their own accounts; admins can update any account.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "user": {
      "firstName": "UpdatedFirstName",
      "lastName": "UpdatedLastName"
    },
    "section_promo": 2
  }
  ```

#### Delete Student

- **Endpoint:** `/api/students/{id}/`
- **Method:** `DELETE`
- **Description:** Deletes a specific student. Students can only delete their own accounts; admins can delete any account.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Get Student Attendance Records

- **Endpoint:** `/api/students/{id}/attendances/`
- **Method:** `GET`
- **Description:** Retrieves all attendance records for a specific student.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Optional Query Parameters:**
  - `subject_id`: Filter by subject ID
  - `date_from`: Filter records on or after this date (YYYY-MM-DD)
  - `date_to`: Filter records on or before this date (YYYY-MM-DD)
  - `status`: Filter by attendance status (present/absent)
- **Response Example:**
  ```json
  [
    {
      "id": 1,
      "date": "2023-05-15",
      "status": "present",
      "student": {
        "id": 5,
        "firstName": "John",
        "lastName": "Doe"
      },
      "subject": {
        "id": 2,
        "name": "Mathematics",
        "teacher": {
          "id": 3,
          "firstName": "Robert",
          "lastName": "Johnson"
        }
      }
    },
    {
      "id": 8,
      "date": "2023-05-16",
      "status": "absent",
      "student": {
        "id": 5,
        "firstName": "John",
        "lastName": "Doe"
      },
      "subject": {
        "id": 3,
        "name": "Biology",
        "teacher": {
          "id": 4,
          "firstName": "Maria",
          "lastName": "Garcia"
        }
      }
    }
  ]

### Attendance API Endpoints

#### Overview

The Attendance API provides endpoints for managing attendance records. Only authenticated users with teacher or admin permissions can create, update, or delete attendance records. Anyone can view the list of attendance records or retrieve details of a specific attendance record.

#### List Attendance Records

- **Endpoint:** `/api/attendance/`
- **Method:** `GET`
- **Description:** Retrieves a list of all attendance records.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Retrieve Attendance Record

- **Endpoint:** `/api/attendance/{id}/`
- **Method:** `GET`
- **Description:** Retrieves details of a specific attendance record.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Create Attendance Record

- **Endpoint:** `/api/attendance/`
- **Method:** `POST`
- **Description:** Creates a new attendance record. Only authenticated users with teacher or admin permissions can create attendance records.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "student": 1,
    "subject": 3,
    "date": "2024-03-15",
    "status": "present"
  }
  ```

#### Update Attendance Record

- **Endpoint:** `/api/attendance/{id}/`
- **Method:** `PATCH`
- **Description:** Updates details of a specific attendance record. Only authenticated users with teacher or admin permissions can update attendance records.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "status": "absent"
  }
  ```

#### Delete Attendance Record

- **Endpoint:** `/api/attendance/{id}/`
- **Method:** `DELETE`
- **Description:** Deletes a specific attendance record. Only authenticated users with teacher or admin permissions can delete attendance records.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Generate Face Encodings

- **Endpoint:** `/api/attendance/generate/`
- **Method:** `POST`
- **Description:** Generates face encodings for a specific promotion/section. This must be done before attempting face recognition for attendance.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "promo_section": "IAGI_PROMO_2026"
  }
  ```

- **Response:**

  ```json
  {
    "message": "Encodings generated successfully for IAGI_PROMO_2026",
    "encoding_path": "encoding/IAGI_PROMO_2026",
    "generated_files": ["123_encodings.pkl", "456_encodings.pkl"]
  }
  ```

#### Process Attendance

- **Endpoint:** `/api/attendance/process/`
- **Method:** `POST`
- **Description:** Processes attendance by recognizing faces in uploaded images.
- **Request Headers:**
  - `Content-Type: multipart/form-data`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  - `images[]`: Image files containing student faces
  - `promo_section`: Name of the promotion/section (e.g., "IAGI_PROMO_2026")
  - `date`: Date in YYYY-MM-DD format

- **Response:**

  ```json
  {
    "date": "2024-03-15",
    "promo_section": "IAGI_PROMO_2026",
    "students": [
      {
        "id": "123",
        "name": "John Doe",
        "status": "present"
      },
      {
        "id": "456",
        "name": "Jane Smith",
        "status": "absent"
      }
    ]
  }
  ```

#### Confirm Attendance

- **Endpoint:** `/api/attendance/confirm/`
- **Method:** `POST`
- **Description:** Confirms and stores attendance records in the database after processing.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
    "date": "2024-03-15",
    "subject": "Mathematics",
    "students": [
      {
        "student_id": "123",
        "status": "present"
      },
      {
        "student_id": "456",
        "status": "absent"
      }
    ]
  }
  ```

- **Response:**

  ```json
  {
    "message": "Attendance successfully recorded",
    "status": "success",
    "records_processed": 2
  }
  ```

### Student Images API Endpoints

#### Overview

The Student Images API provides endpoints for managing student images. Only authenticated users with admin permissions can create, update, or delete student images. A student can only retrieve their own images.

#### List Student Images

- **Endpoint:** `/api/images/?student=<student_id>`
- **Method:** `GET`
- **Description:** Retrieves a list of images for a specific student. A student can only retrieve their own images. Administrators can retrieve images for any student.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Retrieve Student Image

- **Endpoint:** `/api/images/{id}/`
- **Method:** `GET`
- **Description:** Retrieves details of a specific student image.
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`

#### Create Student Image

- **Endpoint:** `/api/images/`
- **Method:** `POST`
- **Description:** Creates new student images (Admin only).
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
- **Request Body:**

  ```json
  {
      "student": 1,
      "images": ["base64_encoded_image_data", ...]
  }
  ```

#### Delete Student Image

- **Endpoint:** `/api/images/{id}/`
- **Method:** `DELETE`
- **Description:** Deletes a specific student image (Admin only).
- **Request Headers:**
  - `Content-Type: application/json`
  - `Cookie: sessionid=<your_session_id>`
  - `X-CSRFToken: <your_csrf_token>`
