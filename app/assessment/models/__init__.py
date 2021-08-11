from flask_sqlalchemy import SQLAlchemy
import uuid as uid
from typing import Union
db = SQLAlchemy()

__all__ = ["customer", "product", "order", "db"]

class UUID(object):
    def __init__(self, uuid:Union[uid.uuid4,str]=None) -> None:
        if uuid:
            self.uuid = uid.UUID(uuid)
        else:
            self.uuid = uid.uuid4()

    def __str__(self) -> str:
        return str(self.uuid)

    def __repr__(self) -> uid.UUID:
        return repr(self.uuid)
