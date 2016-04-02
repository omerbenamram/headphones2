import {Component, Output, EventEmitter, OnInit} from 'angular2/core'
import {Control, FORM_DIRECTIVES} from "angular2/common";
import {Http, Response} from "angular2/http";
import {SearchResult} from "../../../interfaces/search.ts";

@Component({
  selector: 'hp-search',
  directives: [FORM_DIRECTIVES],
  template: require('./search.jade'),
  styles: [require('./search.styl')]
})
export class SearchComponent implements OnInit {
  @Output('on-results')
  onSearchResults = new EventEmitter();

  searchResults:SearchResult[];
  isSearching:boolean;

  input = new Control();

  constructor(private _http:Http) {

  }

  ngOnInit() {
    this.input.valueChanges
      .debounceTime(300)
      .map((input) => `/api/search?type=artist&q=${input}`)
      .do(() => this.isSearching = true)
      .switchMap((queryString) => this._http.get(queryString))
      .map((latestResponse: Response) => latestResponse.json().data)
      .subscribe((latestResultsArray:SearchResult[]) => {
        this.searchResults = latestResultsArray;
        console.log(this.searchResults);
        this.isSearching = false;
        this.onSearchResults.emit(null);
      });
  }
}