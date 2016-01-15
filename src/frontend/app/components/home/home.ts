import {Component} from 'angular2/core';
import {ArtistService} from '../../services/artists/artists';
import {CORE_DIRECTIVES, FORM_DIRECTIVES} from 'angular2/common';
import {Observable} from 'rxjs/Observable';
import {Artist} from '../../interfaces/interfaces';
import {COMMON_DIRECTIVES} from 'angular2/common';
import {ArtworkService} from '../../services/artwork/artwork';

@Component({
  selector: 'home',
  directives: [CORE_DIRECTIVES, FORM_DIRECTIVES, COMMON_DIRECTIVES],
  template: `
  <table id="artist-table" class="table" [hidden]="!artists || artists.length == 0">
    <thead>
      <tr>
        <th>Image</th>
        <th>Artist</th>
        <th>Status</th>
        <th>Total Tracks</th>
      </tr>
    </thead>
    <tbody>
       <tr *ngFor="#artist of artists | async">
         <td><img [src]="artist?.imageUrl | async">
         </td>
         <td>{{artist.name}}</td>
         <td>{{artist.status}}</td>
         <td>{{artist.total_tracks}}</td>
       </tr>
    </tbody>
  </table>
  `,
  styleUrls: ['./components/home/home.css'],
  viewProviders: [ArtistService, ArtworkService]
})
export class HomeCmp {
  public artists:Observable<Artist[]>;

  _artistCallback(artist) {
    artist['imageUrl'] = this.artworkSvc.getArtworkUrl('artist', 'large', artist.id);
    return artist;
  }

  constructor(private artistSvc:ArtistService,
              private artworkSvc:ArtworkService) {
    this.artists = this.artistSvc.getArtists()
      .map((artists:Array<{artist: Artist}>) =>
        artists.map((artist:{artist:Artist}) => this._artistCallback(artist)))
  }
}
