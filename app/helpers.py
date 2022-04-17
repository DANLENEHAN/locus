from sqlalchemy import inspect


def sqlalchemy_obj_to_dict(obj: any) -> dict:
    return {
        x.key:getattr(obj, x.key)
        for x in inspect(obj).mapper.column_attrs
    }