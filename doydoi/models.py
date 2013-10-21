from datetime import datetime

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Query(Base):
    __tablename__ = 'query'
    id = Column(Integer, primary_key=True)
    callback_url = Column(Text)
    callback_id = Column(Text)
    query_data = Column(Text)
    issued_at = Column(DateTime)

    def __init__(self, *args, **kwargs):
        super(Query, self).__init__(*args, **kwargs)
        self.issued_at = datetime.now()

