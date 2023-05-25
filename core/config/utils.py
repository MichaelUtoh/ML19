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


def db_obj_delete(obj, session):
    session.delete(obj)
    session.commit()


def db_bulk_delete(data: list[int], model, session):
    session.exec(delete(model).where(model.id.in_(data.ids)))
    session.commit()


def db_obj_by_id(ids, model, session):
    if type(ids) == int:
        return session.exec(session.query(model).where(model.id == ids)).first()[0]
    elif type(ids) == str and "@" in ids:
        return session.exec(session.query(model).where(model.email == ids)).first()[0]
    elif type(ids) == str:
        return session.exec(session.query(model).where(model.uuid == ids)).first()[0]
    else:
        raise HTTPException(status_code=404, detail="Not found.")


def db_obj_by_uuid(uuid: str, model, session):
    try:
        obj = session.exec(select(model).where(model.uuid == uuid)).first()[0]
        return obj
    except:
        raise HTTPException(status_code=404, detail="Not found.")


def get_qs_by_fkeys(fk, model, session):
    """
    Get product queryset using business foriegn key
    """
    data = session.query(model).all()
    qs = [i for i in data if i.business == fk]
    return qs


def db_queryset(model, session):
    return session.query(model).all()


# def db_queryset(obj, model, session):
#     return session.query(model).where(model.user == obj).all()


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
