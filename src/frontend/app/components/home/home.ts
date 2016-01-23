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
  template: `
  <table id="artist-table" class="table" [hidden]="!artists || artists.length == 0">
    <thead>
      <tr>
        <th>Image</th>
        <th>Artist</th>
        <th>Status</th>
        <th>Latest Album</th>
        <th>Total Tracks</th>
      </tr>
    </thead>
    <tbody>
       <tr *ngFor="#artist of artists | async">
         <td><img [src]="artist?.imageUrl | async">
         </td>
         <td>{{artist.name}}</td>
         <td><span [ngClass]="{'label label-danger': 'artist.status == Wanted'}">{{artist.status}}</span></td>
         <td>{{artist.latest_album}} ({{artist.latest_album_release_date | date:'shortDate'}})</td>
         <td>
           <progress class="progress progress-success" value="10" [max]="artist.total_tracks"></progress>
           <span class="progress-value">{{artist.possessed_tracks}} / {{artist.total_tracks}}</span>
         </td>
       </tr>
    </tbody>
  </table>
  `,
  styleUrls: ['./components/home/home.css'],
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
