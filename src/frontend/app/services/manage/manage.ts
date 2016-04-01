///<reference path="../../../node_modules/rxjs/Observable.d.ts"/>
import {Http} from 'angular2/http';
import {Injectable, Inject} from 'angular2/core';

import {Observable} from "rxjs/Observable";
import 'rxjs/add/operator/map'; //Needed for map to work!
import 'rxjs/add/operator/do';
import {OnInit} from "angular2/core";
import {HeadphonesConfiguration} from "../../interfaces/interfaces.ts";
import {URLSearchParams} from "angular2/http";
import {RequestOptions} from "angular2/http";
import {Headers} from "angular2/http";


@Injectable()
export class ManageService {
    public CONFIGURATION_API:string = '/api/configuration';

    public lastConfiguration:Observable<HeadphonesConfiguration>;

    constructor(@Inject(Http)
                private http:Http) {
    }

    getConfiguration():Observable<HeadphonesConfiguration> {
        return this.http.get(this.CONFIGURATION_API)
            .map(res => res.json())
            .do(x => console.log(x))
    }

    updateConfiguration(configuration:HeadphonesConfiguration):Observable<HeadphonesConfiguration> {
        let body = JSON.stringify(configuration);
        let headers = new Headers({'Content-Type': 'application/json'});
        let options = new RequestOptions({headers: headers});
        console.log('Sending new configuration to server');
        return this.http.put(this.CONFIGURATION_API, body, options)
            .map(res => res.json())
            .do(x => console.log(x));
    }
}
