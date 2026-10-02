from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base, IntPK, CreatedAtType, UpdatedAtType


class LoginModel(Base):
    __tablename__ = "login"

    id : Mapped[IntPK]
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[CreatedAtType]
    updated_at: Mapped[UpdatedAtType]
