///<reference path="../../../node_modules/rxjs/Observable.d.ts"/>
import {Http} from 'angular2/http';
import {Injectable, Inject} from 'angular2/core';

import {Observable} from "rxjs/Observable";
import 'rxjs/add/operator/map'; //Needed for map to work!
import 'rxjs/add/operator/do';
import {OnInit} from "angular2/core";
import {Configuration} from "../../interfaces/interfaces";


@Injectable()
export class ManageService {
  public CONFIGURATION_API:string = '/api/configuration';

  constructor(@Inject(Http) private http:Http) {
  }

  getConfiguration():Observable<Configuration> {
    return this.http.get(this.CONFIGURATION_API)
      .map(res => res.json())
      .do(x => console.log(x));
  }
    updateConfiguration(configuration: LibraryConfiguration) {
        var searchParams:URLSearchParams = new URLSearchParams();
        console.log('Sending new configuration to server');
        for (let t in configuration) {
            console.log(t);
            //searchParams.set(k, v);
        }
        this.http.put(this.CONFIGURATION_API, new RequestOptions({search: searchParams}))
            .map(res => res.json())
    }
}
