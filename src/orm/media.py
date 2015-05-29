from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()

"""
Many to one relation in ascending order.
Artist --> Albums --> Releases --> Tracks
"""


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    musicbrainz_id = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return "<Artist {name}, musicbrainz_id {id}>".format(name=self.name,
                                                             id=self.musicbrainz_id)


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    musicbrainz_id = Column(String, unique=True, nullable=False)

    artist_id = Column(Integer, ForeignKey('artists.id'))
    artist = relationship("Artist", backref=backref('albums', order_by=id))

    def __repr__(self):
        return "<Album {name}, id {id}>".format(name=self.title,
                                                date=self.musicbrainz_id)


class Release(Base):
    __tablename__ = 'releases'

    id = Column(Integer, primary_key=True)
    release_date = Column(DateTime)
    name = Column(String)
    musicbrainz_release_group_id = Column(String, unique=True, nullable=False)
    number_of_tracks = Column(Integer)

    album_id = Column(Integer, ForeignKey('albums.id'))
    album = relationship("Release", backref=backref('releases', order_by=id))

    def __repr__(self):
        return "<Album {album}, release_id {id}>".format(album=self.album,
                                                         id=self.id)


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    title = Column(String)
    number = Column(Integer)
    musicbrainz_id = Column(String, unique=True)
    duration = Column(Integer)
    bitrate = Column(Integer)

    release_id = Column(Integer, ForeignKey('releases.id'))
    release = relationship("Track", backref=backref('tracks', order_by=id))

    def __repr__(self):
        return "<Track {releasename}/{number}-{name}>".format(releasename=self.release.name,
                                                              number=self.number,
                                                              name=self.name)
