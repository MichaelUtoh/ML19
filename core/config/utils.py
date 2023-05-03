from core.celery_app import celery_app


def db_save(obj, session):
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def db_model_delete(model, session):
    session.query(model).delete()
    session.commit()


def db_bulk_delete(ids: list[int], model, session):
    session.query(model).where(model.id.in_(ids)).delete()
    session.commit()


@celery_app.task()
def send_welcome_email_task():
    print("Sending welcome email...")
    return
