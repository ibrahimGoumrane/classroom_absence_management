# Classroom Face Recognition Email Notification

This Django project, includes an email notification system to send HTML-formatted emails to administrators. It leverages Django’s email capabilities with an SMTP backend (e.g., Gmail) and environment variables for secure configuration. This README details the setup and testing of a standalone email function, using the Django shell.

Here’s the Table of Contents (TOC) for your `README.md` based on the provided content. It uses Markdown formatting with clickable links for navigation within the document (assuming it’s viewed in a Markdown renderer that supports TOC linking, like GitHub). Each section is linked to its corresponding heading.

## Table of Contents

- [Classroom Face Recognition Email Notification](#classroom-face-recognition-email-notification)
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Step 1: Set Up the Environment](#step-1-set-up-the-environment)
  - [Step 2: Configure Django Email Settings](#step-2-configure-django-email-settings)
  - [Step 3: Add the Email Function](#step-3-add-the-email-function)
  - [Step 4: Test the Email Function](#step-4-test-the-email-function)

## Project Overview

- **Purpose**: Send HTML-formatted email notifications for classroom face recognition processes.
- **Key Feature**: A standalone `send_email` function to test email delivery.
- **Technologies**:
  - **Django**: Web framework for email sending.
  - **SMTP**: Gmail SMTP server for real email delivery.
  - **Environment Variables**: Secure storage of credentials.

## Project Structure

```
myproject/
├── myproject/
│   ├── __init__.py        # Celery app initialization (if used)
│   ├── settings.py        # Django, Celery, and email configuration
│   ├── urls.py            # URL routing
│   ├── celery.py          # Celery app setup (if used)
│   └── wsgi.py            # WSGI entry point
├── apps/
│   └── students/
│       ├── __init__.py    # App initialization
│       ├── apps.py        # App configuration
│       ├── migrations/    # Database migrations
│       └── tasks.py       # Email and Celery tasks
├── manage.py              # Django management script
├── requirements.txt       # Project dependencies
├── .gitignore             # Git ignore file
└── .env                   # Environment variables (not tracked)
```

## Setup Instructions

### Step 1: Set Up the Environment

1. **Configure Environment Variables**:
   - Create `.env` in the project root:
   
     ```
     MY_EMAIL_ADDRESS=your-email@gmail.com
     MY_EMAIL_APP_PASSWORD=your-app-password
     ADMIN_TEST_EMAIL=admin@example.com
     ```

### Step 2: Configure Django Email Settings

- Edit `myproject/myproject/settings.py`:

  ```python
  # Email Configuration
  EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  EMAIL_HOST = 'smtp.gmail.com'
  EMAIL_PORT = 587
  EMAIL_USE_TLS = True
  EMAIL_HOST_USER = env.str('MY_EMAIL_ADDRESS')  # From .env
  EMAIL_HOST_PASSWORD = env.str('MY_EMAIL_APP_PASSWORD')  # From .env
  DEFAULT_FROM_EMAIL = 'Classroom Face Reco'  # Custom sender name

  # Admin Email
  ADMINS = [('Admin Name', env.str('ADMIN_TEST_EMAIL'))]  # From .env
  ```

### Step 3: Add the Email Function

- Edit `apps/students/tasks.py`:

  ```python
  from django.core.mail import send_mail
  from django.conf import settings

  def send_email():
      """Send an HTML-formatted test email to the admin."""
      subject = 'Test Email'
      plain_message = 'This is a test email sent from classroom face reco project.'
      html_message = '''
      <html>
          <body>
              <h2>Hello from Django!</h2>
              <p>This is a <strong>test email</strong> sent from classroom face reco project.</p>
              <p>This is an example link <a href="https://example.com">link</a>.</p>
          </body>
      </html>
      '''
      from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'test@example.com')
      recipient_list = [admin[1] for admin in getattr(settings, 'ADMINS', [])]
      
      if recipient_list:
          send_mail(
              subject=subject,
              message=plain_message,  # Plain text fallback
              from_email=from_email,
              recipient_list=recipient_list,
              html_message=html_message,
              fail_silently=False,
          )
          print("Email sent successfully!")
      
      return "Email sent successfully"
  ```

### Step 4: Test the Email Function

1. **Start Django Shell**:
   ```powershell
   python manage.py shell
   ```

2. **Run the Function**:
   ```python
   from apps.students.tasks import send_email
   send_email()
   ```

3. **View Output**:
   - **Shell Output**:
     ```
     Email sent.ConcurrentModificationException successfully!
     ```
   - **Email Inbox**:
     - Check the inbox of the email in `ADMIN_TEST_EMAIL` (e.g., `admin@example.com`):
       ```
       Subject: Test Email
       From: Classroom Face Reco <your-email@gmail.com>
       Hello from Django! (in h2)
       This is a test email sent from classroom face reco project. (with "test email" in bold)
       This is an example link link. (clickable link to https://example.com)
       ```
