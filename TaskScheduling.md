# Scheduling a Celery Task Every 20 Seconds in Django with Redis in Docker

This guide walks you through setting up a Django project with Celery to schedule a simple task that prints a message every 20 seconds. It uses Redis as the message broker, running in Docker, and includes all necessary dependency installations and environment configurations. The instructions are tailored for Windows but include notes for Linux/macOS where differences apply.

## Table of Contents

- [Step 1: Install Dependencies](#step-1-install-dependencies)
- [Step 2: Set Up Redis in Docker](#step-2-set-up-redis-in-docker)
- [Step 3: Configure Celery in Django](#step-3-configure-celery-in-django)
- [Step 4: Define the Task](#step-4-define-the-task)
- [Step 5: Apply Migrations](#step-5-apply-migrations)
- [Step 6: Test the Setup](#step-6-test-the-setup)
- [Step 7: Verify Environment](#step-7-verify-environment)
- [Troubleshooting](#troubleshooting)
- [Running the Project](#running-the-project)
- [Notes](#notes)

## Step 1: Install Dependencies

```powershell
pip install celery django-celery-beat redis
```

- `celery`: Core task queue.
- `django-celery-beat`: Periodic task scheduling.
- `redis`: Python client for Redis (for testing).

## Step 2: Set Up Redis in Docker

1. **Pull Redis Image**:

```powershell
 docker pull redis
```

2. **Create and Run Redis Container**:

   ```powershell
   docker run -d --name redis-server -p 6379:6379 redis
   ```

   - `-d`: Detached mode.
   - `--name redis-server`: Container name.
   - `-p 6379:6379`: Maps Redis port to host.
   - `redis`: Official Redis image.

3. **Verify Redis**:
   ```powershell
   docker ps
   ```
   - Look for `redis-server` in the output.
   - Test connection (optional):
     ```powershell
     docker exec -it redis-server redis-cli ping
     ```
     - Expected: `PONG`

## Step 3: Configure Celery in Django

1. **Create `myproject/myproject/celery.py`**:

   ```python
   # myproject/myproject/celery.py
   import os
   from celery import Celery

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
   app = Celery('myproject')
   app.config_from_object('django.conf:settings', namespace='CELERY')
   app.autodiscover_tasks()
   ```

2. **Update `myproject/myproject/__init__.py`**:

   ```python
   # myproject/myproject/__init__.py
   from .celery import app as celery_app
   __all__ = ('celery_app',)
   ```

3. **Update `myproject/myproject/settings.py`**:

   ```python
   # Celery Configuration
   CELERY_BROKER_URL = 'redis://localhost:6379/0'
   CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
   CELERY_ACCEPT_CONTENT = ['json']
   CELERY_TASK_SERIALIZER = 'json'
   CELERY_RESULT_SERIALIZER = 'json'

   # Celery Beat Schedule (every 20 seconds)
   CELERY_BEAT_SCHEDULE = {
       'print-hello-every-20-seconds': {
           'task': 'apps.students.tasks.print_hello',
           'schedule': 20.0,  # 20 seconds
       },
   }

   # Add Celery Beat to Apps
   INSTALLED_APPS = [
       ...
       'django_celery_beat',
   ]
   ```

## Step 4: Define the Task

1. **Create `students/tasks.py`**:

   ```python
   from celery import shared_task

   @shared_task
   def print_hello():
       print("Hello from Celery!")
       return "Task completed"
   ```

## Step 5: Apply Migrations

1. **Run Migrations** (for Celery Beat database tables):
   ```powershell
   python manage.py migrate
   ```

## Step 6: Test the Setup

1. **Start Redis**:

   ```powershell
   docker start redis-server
   ```

   - If not running, use:
     ```powershell
     docker run -d --name redis-server -p 6379:6379 redis
     ```

2. **Start Celery Worker**:

   - Open a terminal:
     ```powershell
     celery -A myproject worker -l info --pool=solo
     ```
   - `--pool=solo`: Ensures compatibility on Windows.

3. **Test Task Manually**:

   - Open another terminal:
     ```powershell
     python manage.py shell
     ```
     ```python
     from apps.students.tasks import print_hello
     print_hello.delay()
     ```
   - Check the worker terminal for:
     ```
     [2025-03-13 22:00:00,000: INFO/MainProcess] Task students.tasks.print_hello[uuid] received
     [2025-03-13 22:00:00,100: INFO/MainProcess] Hello from Celery!
     [2025-03-13 22:00:00,200: INFO/MainProcess] Task students.tasks.print_hello[uuid] succeeded in 0.1s: 'Task completed'
     ```

4. **Start Celery Beat**:
   - Open a third terminal:
     ```powershell
     celery -A myproject beat -l info
     ```
   - Beat logs (scheduling):
     ```
     [2025-03-13 22:00:00,000: INFO/MainProcess] Scheduler: Sending due task print-hello-every-20-seconds (students.tasks.print_hello)
     ```
   - Worker logs (execution every 20 seconds):
     ```
     [2025-03-13 22:00:20,000: INFO/MainProcess] Task students.tasks.print_hello[uuid] received
     [2025-03-13 22:00:20,100: INFO/MainProcess] Hello from Celery!
     ```

## Step 7: Verify Environment

- **Project Structure**:

  ```
  myproject/
  ├── myproject/
  │   ├── __init__.py
  │   ├── settings.py
  │   ├── urls.py
  │   ├── celery.py
  │   └── wsgi.py
  ├── apps/
  │   └── students/
  │       ├── __init__.py
  │       ├── apps.py
  │       ├── migrations/
  │       └── tasks.py
  ├── manage.py
  └── requirements.txt
  ```

- **Dependencies**: Check `requirements.txt` includes:
  ```
  celery>=5.4.0
  django>=4.0
  django-celery-beat>=2.5.0
  redis>=4.0
  ```

## Troubleshooting

- **Redis Not Running**:
  - Check: `docker ps`
  - Restart: `docker restart redis-server`
- **Worker Fails**:
  - Ensure `--pool=solo` on Windows.
  - Debug: `celery -A myproject worker -l debug --pool=solo`
- **No Output**:
  - Worker must be running alongside Beat.
  - Check task name in `CELERY_BEAT_SCHEDULE` matches `tasks.py`.
- **Port Conflict**:
  - Change port: `docker run -d --name redis-server -p 6380:6379 redis`
  - Update `CELERY_BROKER_URL` to `redis://localhost:6380/0`.

## Running the Project

1. Start Redis:
   ```powershell
   docker start redis-server
   ```
2. Start Worker:
   ```powershell
   celery -A myproject worker -l info --pool=solo
   ```
3. Start Beat:
   ```powershell
   celery -A myproject beat -l info
   ```

- **Output**: "Hello from Celery!" printed every 20 seconds in the worker terminal.

## Notes

- **Windows**: Use `--pool=solo` or `--pool=threads` for Celery worker.
- **Linux/macOS**: Omit `--pool=solo` (default `prefork` works).
- **Scaling**: Increase `schedule` (e.g., `604800` for weekly) as needed.
