import {Http} from '@angular/http';
import {Injectable, Inject} from '@angular/core';
import {Observable} from "rxjs/Observable";
import {Artist} from './artist.model.ts';

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
