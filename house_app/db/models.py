from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from house_app.db.database import Base



class House(Base):
    __tablename__ = "house"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    area: Mapped[int] = mapped_column(Integer)
    year: Mapped[int] = mapped_column(Integer)
    garage: Mapped[int] = mapped_column(Integer)
    total_basement: Mapped[int] = mapped_column(Integer)
    bath: Mapped[int] = mapped_column(Integer)
    overall_quality: Mapped[int] = mapped_column(Integer)
    neighborhood: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


