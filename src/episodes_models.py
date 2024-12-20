from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base


# модель для сохранения данный в БД
class Episodes(Base):
    __tablename__ = ''

    id: Mapped[int] = mapped_column (primary_key=True)
    tags: Mapped[str]
    name: Mapped[str]
    preview: Mapped[str]
    content: Mapped[str]
