///<reference path="../../../node_modules/rxjs/Observable.d.ts"/>
import {Http} from 'angular2/http';
import {Injectable, Inject} from 'angular2/core';
import 'rxjs/add/operator/map'; //Needed for map to work!
import {Artist} from "../../interfaces/interfaces";
import {ArtworkService} from "../artwork/artwork";
import {Observable} from "rxjs/Observable";
import 'rxjs/add/operator/toArray'
import 'rxjs/add/operator/do'

@Injectable()
export class ArtistService {
  public ARTISTS_API:string = '/api/artists';

  constructor(@Inject(Http) private http:Http,
              @Inject(ArtworkService) private artworkSvc:ArtworkService) {
  }

  getArtists():Observable<any> {
    return this.http.get('/api/artists')
      .map(res => res.json())
      .do(x => console.log("Call to artists returned" + x));
  }
}
