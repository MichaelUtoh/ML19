# Helper functions


def db_save(obj, session):
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj
