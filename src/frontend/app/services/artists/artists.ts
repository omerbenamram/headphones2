import {Http} from 'angular2/http';
import {Injectable, Inject} from 'angular2/core';
import {Observable} from "rxjs/Observable";
import {Artist} from '../../interfaces/interfaces.ts';

@Injectable()
export class ArtistService {
  public ARTISTS_API:string = '/api/artists';

  constructor(private http:Http) {
  }

  getArtists():Observable<Artist[]> {
    return this.http.get(this.ARTISTS_API)
      .map(res => res.json().data)
      .do(x => console.log(x));
  }
}
