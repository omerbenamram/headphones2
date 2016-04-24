import {Http, RequestOptions, Headers} from "angular2/http";
import {Injectable, Inject} from "angular2/core";
import {Observable} from "rxjs/Observable";
import {HeadphonesConfiguration} from "../../interfaces/interfaces.ts"


@Injectable()
export class ManageService {
    public CONFIGURATION_API:string = '/api/configuration';

    public lastConfiguration:Observable<HeadphonesConfiguration>;

    constructor(@Inject(Http)
                private http:Http) {
    }

    getConfiguration():Observable<HeadphonesConfiguration> {
        return this.http.get(this.CONFIGURATION_API)
            .map(res => res.json().data.data)
            .do(res => console.log(res))
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
