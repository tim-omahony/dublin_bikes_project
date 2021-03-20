from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

Base = declarative_base()

class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    temp = Column(Float)
    last_update = Column(DateTime)

    def to_json(self):
        return dict(id=self.id, description=self.description, temp=self.temp, last_update=self.last_update.isoformat())
