from sqlalchemy import delete, select
from fastapi import HTTPException

from core.models.accounts import User


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
    try:
        obj = session.exec(select(model).where(model.uuid == uuid)).first()[0]
        return obj
    except:
        raise HTTPException(status_code=404, detail="Not found.")


def db_obj_by_fkeys(fk, model, session):
    """
    Get queryset using foriegn keys
    """
    data = session.exec(session.query(model).where(model.business == fk)).all()
    return data


def business_location_func(businesses: list, session):
    from core.models.businesses import Location

    for idx in businesses:
        idx.open_days = idx.open_days.strip("{}").split(",")
        idx.location = (
            session.query(Location).where(Location.id == idx.location_id).first()
        )


def get_db_user(email: str, session):
    user = session.query(User).where(User.email == email).first()
    if user:
        return user
    return None
