from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class Product(Base):
    __tablename__ = "product"
    id = Column(UUID(as_uuid=True), primary_key=True)
    dataframe = Column(String)

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, dataframe={self.dataframe!r})"