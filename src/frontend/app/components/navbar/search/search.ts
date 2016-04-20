import {Component, Output, EventEmitter, OnInit, ViewChildren, QueryList, AfterViewInit} from "angular2/core";
import {Control, FORM_DIRECTIVES} from "angular2/common";
import {Http, Response} from "angular2/http";
import {SearchResult} from "../../../interfaces/search.ts";
import {SearchResultCmp} from "./searchResult.ts";
import {KeyEventsPlugin} from "angular2/src/platform/dom/events/key_events";

@Component({
  selector: 'hp-search',
  directives: [FORM_DIRECTIVES, SearchResultCmp],
  template: require('./search.jade'),
  styles: [require('./search.styl')]
})
export class SearchComponent implements OnInit, AfterViewInit {
  @Output('on-results')
  onSearchResults = new EventEmitter();

  //noinspection TypeScriptValidateTypes
  @ViewChildren(SearchResultCmp)
  searchResultsCmpsQuery:QueryList<SearchResultCmp>;
  searchResultsCmps:SearchResultCmp[];

  selectedActionIndex:number;

  showSearchResults:boolean = false;
  searchResults:SearchResult[];
  isSearching:boolean = false;

  input = new Control();

  mode:string = "artist";

  constructor(private _http:Http) {

  }

  onMouseLeave($event) {
    if (this.showSearchResults == true) {
      this.showSearchResults = false;
    }
  }

  onMouseEnter($event){
    if (this.showSearchResults == false && this.searchResults != []) {
      this.showSearchResults = true;
    }
  }

  onInputArrowDown($event) {
    let keyCombination = KeyEventsPlugin.getEventFullKey($event);
    if (keyCombination == 'arrowDown') {
      this.selectedActionIndex = 0;
      this.searchResultsCmps[this.selectedActionIndex].focus();
      $event.preventDefault();
    }
  }

  onActionChanged($event) {

  }

  onActionSelected($event) {

  }

  ngAfterViewInit() {
    this.searchResultsCmpsQuery.changes.subscribe(() => {
        this.searchResultsCmps = this.searchResultsCmpsQuery.toArray();
        console.log(this.searchResultsCmps);
      }
    )
  }

  ngOnInit() {
    this.input.valueChanges
      .debounceTime(300)
      .filter((input:string) => input.length >= 1)
      .map((input) => `/api/search?type=${this.mode}&q=${input}`)
      .do(() => {
        this.searchResults = [];
        this.isSearching = true
      })
      .switchMap((queryString) => this._http.get(queryString))
      .map((latestResponse:Response) => latestResponse.json().data)
      .subscribe((latestResultsArray:SearchResult[]) => {
        this.searchResults = latestResultsArray;
        console.log(this.searchResults);
        this.isSearching = false;
        this.showSearchResults = true;
      });
  }
}