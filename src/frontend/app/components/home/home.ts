import {Component} from 'angular2/core';
import {ArtistService} from '../../services/artists/artists';
import {CORE_DIRECTIVES, FORM_DIRECTIVES} from 'angular2/common';
import {Observable} from 'rxjs/Observable';
import {Artist} from '../../interfaces/interfaces';
import {COMMON_DIRECTIVES} from 'angular2/common';
import {ArtworkService} from '../../services/artwork/artwork';
import {NgClass} from 'angular2/common';
import {NgStyle} from 'angular2/common';

@Component({
  selector: 'home',
  directives: [CORE_DIRECTIVES, FORM_DIRECTIVES, COMMON_DIRECTIVES, NgClass, NgStyle],
  template: require('./home.jade'),
  styles: [require('./home.styl')],
  viewProviders: [ArtistService, ArtworkService]
})
export class HomeCmp {
  public artists:Observable<Artist[]>;

  _artistCallback(artist: Artist) {
    artist['imageUrl'] = this.artworkSvc.getArtworkUrl('artist', 'large', artist.id);
    artist['latest_album_release_date'] = Date.parse(artist.latest_album_release_date);
    return artist;
  }

  constructor(private artistSvc:ArtistService,
              private artworkSvc:ArtworkService) {
    this.artists = this.artistSvc.getArtists()
      .map((artists:Array<{artist: Artist}>) =>
        artists.map((artist:{artist:Artist}) => this._artistCallback(artist)));
  }
}
