import {Component} from 'angular2/core';
import {ArtistService} from '../../services/artists/artists';
import {CORE_DIRECTIVES, FORM_DIRECTIVES} from 'angular2/common';
import {OnInit} from 'angular2/core';

@Component({
  selector: 'home',
  templateUrl: './components/home/home.html',
  styleUrls: ['./components/home/home.css'],
  directives: [CORE_DIRECTIVES, FORM_DIRECTIVES],
  viewProviders: [ArtistService]
})
export class HomeCmp implements OnInit {
  constructor(private _artistService:ArtistService) {  }
  artists = [];

  debugMe() {
    debugger;
  }

  ngOnInit() {
    this.artists = this._artistService.getArtists();
  }
}
