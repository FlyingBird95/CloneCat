from sqlalchemy import String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class Foo(Base):
    __tablename__ = "foo"

    id: Mapped[int] = mapped_column(primary_key=True)
    bar: Mapped[str] = mapped_column(String(100))
