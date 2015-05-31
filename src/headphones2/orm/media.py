from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum

Base = declarative_base()

'''
Many to one relation in ascending order.
Artist --> Albums --> Releases --> Tracks
'''
STATUSES = ['wanted', 'skipped', 'ignored', 'downloaded']


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    musicbrainz_id = Column(String, unique=True, nullable=False)

    status = Column(Enum(*STATUSES))

    albums = relationship('Album', lazy='dynamic')

    def __repr__(self):
        return '<Artist {name} ({id})>'.format(name=self.name,
                                               id=self.musicbrainz_id)


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    musicbrainz_id = Column(String, unique=True, nullable=False)
    type = Column(String)
    status = Column(Enum(*STATUSES))

    artist_id = Column(Integer, ForeignKey('artists.id'))
    artist = relationship('Artist')

    releases = relationship('Release', lazy='dynamic')

    def __repr__(self):
        return '<Album {name} ({id})>'.format(name=self.title,
                                              id=self.musicbrainz_id)


class Release(Base):
    __tablename__ = 'releases'

    id = Column(Integer, primary_key=True)
    release_date = Column(DateTime)
    title = Column(String)
    asin = Column(String)
    musicbrainz_id = Column(String, unique=True, nullable=False)

    album_id = Column(Integer, ForeignKey('albums.id'))
    album = relationship('Album')

    tracks = relationship('Track', lazy='dynamic')

    def __repr__(self):
        return '<Album {album} ({id})>'.format(album=self.album,
                                               id=self.id)


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    title = Column(String)
    number = Column(Integer)
    media_number = Column(Integer)

    musicbrainz_id = Column(String, unique=True)
    length = Column(Integer)
    bitrate = Column(Integer)

    location = Column(String)
    matched = Column(String)
    format = Column(String)

    release_id = Column(Integer, ForeignKey('releases.id'))
    release = relationship('Release')

    def __repr__(self):
        return '<Track {releasename}[{number}] {name} ({id})>'.format(releasename=self.release.name,
                                                                      number=self.number,
                                                                      name=self.name,
                                                                      id=self.musicbrainz_id)
