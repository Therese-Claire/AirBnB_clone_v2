#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, Float, String,\
        ForeignKey, MetaData, Table
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity
import models


metadata = Base.metadata
place_amenity = Table(
    'place_amenity', metadata,
    Column('place_id', String(60), ForeignKey('places.id'), PrimaryKey=True),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           PrimaryKey=True)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'))
    user_id = Column(String(60), ForeignKey('users.id'))
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship('Review', cascade='all, delete, delete-orphan',
                           backref='place')
    amenities = relationship('Amenity', secondary='place_amenity',
                             viewonly='False')

    @property
    def reviews(self):
        """ Returns the list of Review instances with place_id equals
            to the current Place.id """
        instances = []
        result = []
        temp = models.storage.all()
        for key in temp.keys():
            if key.startswith('Review.'):
                instances.append(temp[key])
        for instance in instances:
            if instance.place_id == self.id:
                result.append(instance)
        return result

    @property
    def amenities(self):
        """ returns the list of Amenity instances based on the attribute
            amenity_ids that contains all Amenity.id linked to the Place """
        return self.amenity_ids

    @amenities.setter
    def amenities(sel, obj=None):
        if isinstance(obj, Amenity) and obj.id not in amenity_ids:
            self.amenity_ids.append(obj.id)
