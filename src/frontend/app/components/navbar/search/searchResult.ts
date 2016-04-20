import {Component, Input, ElementRef, Output, EventEmitter} from "angular2/core";
import {SearchResult} from "../../../interfaces/search.ts";
@Component({
  selector: 'hp-search-result',
  template: require('./searchResult.jade'),
  styles: [require('./search.styl'), require('./searchResult.styl')]
})
export class SearchResultCmp {
  @Input('result')
  result:SearchResult;

  @Output('on-selected')
  onSelected = new EventEmitter<SearchResult>();

  constructor(private _el:ElementRef) {

  }

  focus() {
    this._el.nativeElement.focus();
  }

  onClick($event:MouseEvent) {
    this.focus();
    $event.stopImmediatePropagation();
    $event.preventDefault();
  }

}