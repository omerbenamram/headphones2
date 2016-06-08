import {Component, Output, EventEmitter, OnInit, ViewChildren, QueryList, AfterViewInit} from "@angular/core";
import {Control, FORM_DIRECTIVES} from "@angular/common";
import {Http, Response} from "@angular/http";
import {SearchResult} from "../interfaces/search.ts";
import {SearchResultCmp} from "./searchResult.component.ts";

@Component({
  selector: 'hp-search',
  directives: [FORM_DIRECTIVES, SearchResultCmp],
  template: require('./search.component.pug'),
  styles: [require('./search.component.styl')]
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

  onMouseEnter($event) {
    if (this.showSearchResults == false && this.searchResults != []) {
      this.showSearchResults = true;
    }
  }

  onInputArrowDown($event:KeyboardEvent) {
    this.selectedActionIndex = 0;
    this.refoucsResults($event)
  }

  refoucsResults($event):void {
    this.searchResultsCmps[this.selectedActionIndex].focus();
    $event.stopImmediatePropagation();
    $event.preventDefault();
  }

  onResultArrowDown($event:KeyboardEvent) {
    let lastIndex = this.searchResultsCmps.length - 1;
    if (this.selectedActionIndex < lastIndex) {
      this.selectedActionIndex += 1;
      this.refoucsResults($event);
    }
  }

  onResultArrowUp($event:KeyboardEvent) {
    if (this.selectedActionIndex > 0) {
      this.selectedActionIndex -= 1;
      this.refoucsResults($event);
    }
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