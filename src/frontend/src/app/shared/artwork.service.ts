import {Http, RequestOptions, URLSearchParams} from "@angular/http";
import {Injectable, Inject} from "@angular/core";
import {Observable} from "rxjs/Observable";

@Injectable()
export class ArtworkService {

  public ARTWORK_API:string = '/api/artwork';

  constructor(private http:Http) {
  }

  getArtworkUrl(type:string, size:string, id:string):Observable<any> {
    var searchParams:URLSearchParams = new URLSearchParams();
    searchParams.set('type', type);
    searchParams.set('size', size);
    searchParams.set('id', id);

    return this.http
      .get(this.ARTWORK_API, new RequestOptions({search: searchParams}))
      .map((res:any) => res.json().data);
  }
}
