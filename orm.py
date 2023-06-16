"""
This module defines the data layer, and how it maps onto the domain layer.

We use SQLAlchemy's "imperative mapping" feature so the data layer depends on the domain layer (not
the other way around).

See https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#imperative-mapping for docs on this
manual mapping style.
"""
from sqlalchemy import Column, Date, Float, Integer, String, Table
from sqlalchemy.orm import registry

import model

mapper_registry = registry()


talks_table = Table(
    "talks",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("ref", String(512), unique=True),
    Column("title", String(512)),
    Column("description", String(512)),
    Column("event_date", Date),
    Column("score", Float),
)


def register_mappers() -> None:
    """
    Map the table classes to the domain models.
    """
    mapper_registry.map_imperatively(model.Talk, talks_table)
