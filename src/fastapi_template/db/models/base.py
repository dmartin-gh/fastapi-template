from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.schema import MetaData


class Base(DeclarativeBase):
    metadata = MetaData(
        # https://alembic.sqlalchemy.org/en/latest/naming.html
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
