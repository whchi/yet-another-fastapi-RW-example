from app.core import get_db_settings
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, create_engine

engine = create_engine(
    url=get_db_settings().connection_string,
    echo=True,
    future=True,
)

session_global = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
    expire_on_commit=False,
)


def get_session():  # type: ignore
    # sqlalchemy always run statements in a transaction
    # @see https://github.com/sqlalchemy/sqlalchemy/discussions/6921
    with session_global() as session:
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
