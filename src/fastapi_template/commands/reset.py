from alembic.config import Config as AlembicConfig
from alembic import command as alembic_cmd
from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
import click
import logging.config

from fastapi_template.db.models import Base
from fastapi_template.settings import Settings


async def db_reset(uri: PostgresDsn):
    engine = create_async_engine(uri)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


@click.command("reset")
@click.option("-v", "--verbose", is_flag=True, help="enable verbose logging")
def main(verbose: bool):
    """
    Drop all existing objects from the database and recreate them.
    """

    logging.basicConfig()
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "loggers": {
                "sqlalchemy.engine.Engine": {"level": "INFO" if verbose else "WARN"},
            },
        }
    )

    settings = Settings()
    click.echo(f"Resetting database: {settings.SQLALCHEMY_DATABASE_URI}")
    asyncio.run(db_reset(settings.SQLALCHEMY_DATABASE_URI))

    alembic_cfg = AlembicConfig(f"{settings.ALEMBIC_DIR}/alembic.ini")
    alembic_cfg.set_main_option("script_location", f"{settings.ALEMBIC_DIR}/migrations")
    alembic_cmd.stamp(alembic_cfg, "head")
    alembic_cmd.current(alembic_cfg, verbose=verbose)
