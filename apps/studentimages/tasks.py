from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def print_hello():
    print("Hello from Celery!")
    return "Task completed"

@shared_task
def print_time():
    print("Ran at a scheduled time!")
    return "Task completed"

def send_email():
    subject = 'Test Email'
    plain_message = 'This is a test email sent from classroom face reco project.'
    html_message =  '''
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
    
    # send_mail with html_message sends a multipart/alternative email,
    # including both plain text and HTML for clients that don’t support HTML.
    if recipient_list:
        send_mail(
            subject=subject,
            message=plain_message, # fallback message
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
    
    return "Email sent successfully"