from sqlalchemy import Table, Column, Integer, Float, String, DateTime
from sqlalchemy import create_engine, MetaData
import datetime as dt
import os

engine = create_engine(os.getenv("DATABASE_JDBC", "sqlite:///:memory:"))
metadata_obj = MetaData()

product = Table(
    "product",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(512), nullable=False),
    Column("source", String(16), nullable=False),
    Column("price", Float, nullable=False),
    Column(
        "created_at", DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    ),
    Column("product_type", String(16), nullable=False),
)

real_estate = Table(
    "real_estate",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String),
    Column("url", String),
    Column("source", String),
    Column("price", Float),
    Column("description", String),
    Column("type", String),
    Column("type_extended", String),
    Column("location", String),
    Column("square_m", Float),
    Column("square_property_m", Float),
    Column("wood_shed", String, nullable=True),
    Column("garage", String, nullable=True),
    Column("parking", String, nullable=True),
    Column("balcony", String, nullable=True),
    Column(
        "created_at", DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    ),
)
