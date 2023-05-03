from core.celery_app import celery_app


@celery_app.task()
def send_welcome_email_task():
    print("Sending welcome email...")
    return
