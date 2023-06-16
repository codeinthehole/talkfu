from sqlalchemy import Column, Date, Float, Integer, String, Table
from sqlalchemy.orm import registry

import model

# See https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#imperative-mapping
# for docs on this manual mapping style.


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
    mapper_registry.map_imperatively(model.Talk, talks_table)
