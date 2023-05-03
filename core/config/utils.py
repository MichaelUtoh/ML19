from sqlalchemy import delete


def db_save(obj, session):
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def db_model_delete(model, session):
    session.query(model).delete()
    session.commit()


def db_bulk_delete(data: list[int], model, session):
    session.exec(delete(model).where(model.id.in_(data.ids)))
    session.commit()
