from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy_utils import ChoiceType

Base = declarative_base()

'''
Many to one relation in ascending order.
Artist --> Albums --> Releases --> Tracks --> MediaFile
'''


class Status(enum.Enum):
    Wanted = 1
    Skipped = 2
    Ignored = 3
    Snatched = 4
    Downloaded = 5

    @classmethod
    def from_name(cls, name):
        for status in cls:
            if status.name == name:
                return status

        raise ValueError('{name} is not a valid {cls_name}'.format(name=name, cls_name=cls.__name__))


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    musicbrainz_id = Column(String, unique=True, nullable=False)

    status = Column(ChoiceType(Status, impl=Integer()))

    albums = relationship('Album', lazy='dynamic', cascade="delete")

    def __repr__(self):
        return '<Artist {name} ({id})>'.format(name=self.name,
                                               id=self.musicbrainz_id)


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    musicbrainz_id = Column(String, unique=True, nullable=False)
    type = Column(String)
    status = Column(ChoiceType(Status, impl=Integer()))

    artist_id = Column(Integer, ForeignKey('artists.id'))
    artist = relationship('Artist')

    releases = relationship('Release', lazy='dynamic', cascade="delete")

    def __repr__(self):
        return '<Album {name} ({id})>'.format(name=self.title,
                                              id=self.musicbrainz_id)


class Release(Base):
    __tablename__ = 'releases'

    id = Column(Integer, primary_key=True)
    release_date = Column(DateTime)
    title = Column(String)
    asin = Column(String, default='')
    country = Column(String, default='')
    musicbrainz_id = Column(String, unique=True, nullable=False)

    is_selected = Column(Boolean, default=False)

    album_id = Column(Integer, ForeignKey('albums.id'))
    album = relationship('Album')

    tracks = relationship('Track', lazy='dynamic', cascade="delete")

    @hybrid_property
    def length(self):
        return sum(track.length for track in self.tracks)

    @hybrid_property
    def average_bitrate(self):
        tracks = [track.bitrate for track in self.tracks]
        return sum(tracks) / len(tracks)

    def __repr__(self):
        return '<Release {album} - Released in {date},' \
               ' {country} - {tracks} Tracks ({id})>'.format(album=self.album.title,
                                                             date=self.release_date,
                                                             tracks=self.tracks.count(),
                                                             country=self.country,
                                                             id=self.id)


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    number = Column(Integer)
    media_number = Column(Integer)

    # Tracks can have same musicbrainz_id (however they are unique per release)
    musicbrainz_id = Column(String, unique=False)
    length = Column(Integer)

    release_id = Column(Integer, ForeignKey('releases.id'))
    release = relationship('Release')

    def __repr__(self):
        return '<Track {releasename}[{number}] {name} ({id})>'.format(releasename=self.release.title,
                                                                      number=self.number,
                                                                      name=self.title,
                                                                      id=self.musicbrainz_id)


class MediaFile(Base):
    __tablename__ = 'mediafiles'
    id = Column(Integer, primary_key=True)
    path = Column(String)

    bitrate = Column(Integer, nullable=True)
    # TODO: this should be an inferred attribute
    format = Column(String)

    track_id = Column(Integer, ForeignKey('tracks.id'))
    track = relationship('Track', backref='files')

    release_id = Column(Integer, ForeignKey('releases.id'))
    release = relationship('Release')

    def __repr__(self):
        return "<MediaFile {track_name} at {path}>".format(track_name=self.track.title,
                                                           path=self.path)
