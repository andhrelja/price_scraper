from sqlalchemy import Table, Column, Integer, Float, String, DateTime
from sqlalchemy import create_engine, MetaData
import datetime as dt

engine = create_engine('sqlite:///:memory:')
metadata_obj = MetaData()

product = Table(
    'product',
    metadata_obj,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(512), nullable=False),
    Column('source', String(16), nullable=False),
    Column('price', Float, nullable=False),
    Column('created_at', DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)),
)