///<reference path="../../../node_modules/rxjs/Observable.d.ts"/>
import {Http} from 'angular2/http';
import {Injectable, Inject} from 'angular2/core';
import 'rxjs/add/operator/map'; //Needed for map to work!
import {Artist} from "../../interfaces/interfaces";

@Injectable()
export class ArtistService {
  public artists:Array<Artist> = [];
  public ARTISTS_API:string = '/api/artists';
  public ARTWORK_API:string = '/api/artwork/artist';

  private _http:any;

  @Inject(Http)
  constructor(private http:Http) {
    this._http = http;
  }

  _getArtistArtworkUrl(artist_id, size:'large'):string {
    return `${this.ARTWORK_API}/${artist_id}/${size}`
  }

  getArtists() {
    this._http.get('/api/artists')
      .map(res => res.json())
      .subscribe(
        data => this.addData(data),
        err => console.log('Exception!' + err),
        () => console.log(`Fetched`)
      );
    return this.artists;
  };

  addData(data) {
    console.log(data);
    // TODO: make sure this is changed later when API is modified
    data['aaData'].forEach((row) => {
      row['imageUrl'] = this._getArtistArtworkUrl(row['ArtistID'], 'large');
      this.artists.push(row);
    });
  }


}
