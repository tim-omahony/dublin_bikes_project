from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

Base = declarative_base()


class Station(Base):
        __tablename__ = 'stations'

        id = Column(Integer, primary_key=True)
        address = Column(String)
        banking = Column(Integer)
        bike_stands = Column(Integer)
        bonus = Column(Integer)
        contract_name = Column(String)
        name = Column(String)
        number = Column(Integer)
        position_lat = Column(Float)
        position_lng = Column(Float)
        status = Column(String)
        available_bikes = Column(Integer)
        available_bike_stands = Column(Integer)
        last_update = Column(DateTime)

        def to_json(self):
            return dict(id=self.id, address=self.address, banking=self.banking, bike_stands=self.bike_stands,
                        bonus=self.bonus, contract_name=self.contract_name, name=self.name, number=self.number,
                        position_lat=self.position_lat, position_lng=self.position_lng, status=self.status,
                        available_bikes=self.available_bikes, available_bike_stands=self.available_bike_stands, last_update=self.last_update.isoformat()
                        )