import {Component, OnInit} from 'angular2/core';
import {ArtistService} from '../../services/artists/artists';
import {CORE_DIRECTIVES, FORM_DIRECTIVES} from 'angular2/common';
import {Observable} from 'rxjs/Observable';
import {Artist} from '../../interfaces/interfaces';
import {COMMON_DIRECTIVES} from "angular2/common";

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
        <th>Total Track</th>
      </tr>
    </thead>
    <tbody>
       <tr *ngFor="#artist of artists">
         <td>
           <img [src]='artist?.imageUrl' width="80" height="80" [hidden]="!artist.imageUrl">
         </td>
         <td>{{artist.ArtistName}}</td>
         <td>{{artist.Status}}</td>
         <td>{{artist.TotalTracks}}</td>
       </tr>
    </tbody>
  </table>

  `,
  styleUrls: ['./components/home/home.css'],
  viewProviders: [ArtistService]
})
export class HomeCmp implements OnInit {
  public artists:Array<any>;

  constructor(private _artistService:ArtistService) {
  }

  ngOnInit() {
    this.artists = this._artistService.getArtists();
  }
}
