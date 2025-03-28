from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from pathlib import Path
from detector import FaceRecognitionHandler
from apps.users.models import User
from apps.studentimages.models import StudentImage


@shared_task
def print_hello():
    print("Hello from Celery!")
    return "Task completed"


def send_notification_to_admins(subject, plain_message, html_message=None):
    # Fetch emails of active admins
    admin_emails = User.objects.filter(role='admin', is_active=True).values_list('email', flat=True)

    if admin_emails:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=list(admin_emails),  # Convert QuerySet to list
            html_message=html_message,
            fail_silently=False,  # Raise exception if sending fails
        )


@shared_task
def encode_new_images_task():
    face_handler = FaceRecognitionHandler()

    images_to_process = StudentImage.objects.filter(is_encoded=False).count()

    if images_to_process == 0:
        subject = "Reencoding Skipped - No New Images"
        plain_message = "No new images were found to encode."
        html_message = """
        <html>
            <body>
                <h2>Reencoding Skipped</h2>
                <p>No new images were found to encode.</p>
            </body>
        </html>
        """
        send_notification_to_admins(subject, plain_message, html_message)
        return "No new images to encode."

    try:
        encoded_image_ids = face_handler.encode_known_faces()

        encoded_ids_count = len(encoded_image_ids)

        plain_message = (
            f"The reencoding of {encoded_ids_count} new image(s) has been completed successfully.\n\n"
            "Encoded Image IDs:\n" + "\n".join([f"- {image_id}" for image_id in encoded_image_ids])
        )

        html_message = f"""
        <html>
            <body>
                <h2>Reencoding Completed</h2>
                <p>The reencoding of {encoded_ids_count} new image(s) has been completed successfully.</p>
                <h3>Encoded Image IDs</h3>
                <table border="1" style="border-collapse: collapse;">
                    <thead>
                        <tr>
                            <th style="padding: 8px;">Image ID</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f'<tr><td style="padding: 8px;">{image_id}</td></tr>' for image_id in encoded_image_ids])}
                    </tbody>
                </table>
            </body>
        </html>
        """

        subject = "Reencoding Completed Successfully"

        send_notification_to_admins(subject, plain_message, html_message)

        return "Reencoding completed successfully"

    except Exception as e:
        # Send error notification
        subject = "Reencoding Failed"
        plain_message = f"An error occurred during the reencoding process: {str(e)}"
        html_message = f"""
        <html>
            <body>
                <h2>Reencoding Failed</h2>
                <p>An error occurred during the reencoding process: {str(e)}</p>
            </body>
        </html>
        """

        send_notification_to_admins(subject, plain_message, html_message)

        # Re-raise the exception for Celery to handle
        raise
