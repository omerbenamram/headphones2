from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()

class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    asin = Column(String)
    release_date = Column(DateTime)
    musicbrainz_id = Column(String)
    musicbrainz_release_group_id = Column(String, nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.id'))

    artist = relationship("Artist", backref=backref('albums', order_by=id))

    def __repr__(self):
        return "<Album {name}, released in {date}, release_group_id {id}>".format(name=self.title,
                                                                                  date=self.release_date,
                                                                                  id=self.musicbrainz_release_group_id)

class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    musicbrainz_id = Column(String)

    def __repr__(self):
        return "<Artist {name}, musicbrainz_id {id}>".format(name=self.name,
                                                             id=self.musicbrainz_id)