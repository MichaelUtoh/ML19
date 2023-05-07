from sqlalchemy import delete, select
from fastapi import HTTPException


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


def db_obj_by_id(ids: int, model, session):
    obj = session.exec(session.query(model).where(model.id == ids))
    if not obj:
        raise HTTPException(status_code=404, detail="Not found.")
    return obj


def db_obj_by_uuid(uuid: str, model, session):
    obj = session.exec(select(model).where(model.uuid == uuid)).first()[0]
    if not obj:
        raise HTTPException(status_code=404, detail="Not found.")
    return obj
