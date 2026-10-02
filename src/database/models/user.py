from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base, NameType, EmailType, PasswordType, IntPK, CreatedAtType, UpdatedAtType


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[IntPK]
    username: Mapped[NameType] = mapped_column(unique=True)
    age: Mapped[int]
    email: Mapped[EmailType] = mapped_column(unique=True)
    password: Mapped[PasswordType]
    created_at: Mapped[CreatedAtType]
    updated_at: Mapped[UpdatedAtType]



