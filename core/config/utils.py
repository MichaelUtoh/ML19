from core.celery_app import celery_app


def db_save(obj, session):
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@celery_app.task()
def send_welcome_email_task():
    print("Sending welcome email...")
    return
