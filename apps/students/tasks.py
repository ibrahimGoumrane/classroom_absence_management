from celery import shared_task

@shared_task
def print_hello():
    print("Hello from Celery!")
    return "Task completed"

@shared_task
def print_time():
    print("Ran at a scheduled time!")
    return "Task completed"