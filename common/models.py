"""Common metaclasses and types to create SQLAlchemy-type model."""

from sqlalchemy.orm import declarative_base  # type: ignore


TableModel = declarative_base()
