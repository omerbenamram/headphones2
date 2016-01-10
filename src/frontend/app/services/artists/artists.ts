///<reference path="../../../node_modules/rxjs/Observable.d.ts"/>
import {Injectable} from 'angular2/core';
import {HTTP_PROVIDERS, Http} from 'angular2/http';
import {Component} from 'angular2/core';
import {Inject} from "angular2/core";
import 'rxjs/add/operator/map';


@Injectable()
export class ArtistService {
  artists = [];

  constructor(@Inject(Http) http:Http) {
    http.get('/getArtists.json')
      .map(res => res.json())
      .subscribe(
        data => this.addData(data),
        err => this.logError(err),
        () => console.log("THIS" + this.artists)
      );
  }

  addData(data) {
    console.log(data);
    data['aaData'].forEach((row) => {
      this.artists.push(row);
    })
  }

  logError(err) {
    console.error('There was an error: ' + err);
  }

  getArtists = function () {
    return this.artists;
  };
}
