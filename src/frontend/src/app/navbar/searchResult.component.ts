import {Component, Input, ElementRef, Output, EventEmitter} from "@angular/core";
import {SearchResult} from "../interfaces/search.ts";
import {ArtworkService} from "../shared/artwork.service.ts";

@Component({
  selector: '[hp-search-result]',
  template: require('./searchResult.component.pug'),
  styles: [require('./search.component.styl'), require('./searchResult.component.styl')],
  viewProviders: [ArtworkService]
})
export class SearchResultCmp {
  @Input('result')
  result:SearchResult;

  @Output('on-selected')
  onSelected = new EventEmitter<SearchResult>();
  imgUrl:string;

  constructor(private _el:ElementRef, private _artworkSvc:ArtworkService) {
  }

  ngOnInit() {
    this._artworkSvc.getArtworkUrl('artist', 'small', this.result.id).subscribe((result) => {
      this.imgUrl = result;
    });
  }

  focus() {
    this._el.nativeElement.getElementsByClassName('search-result')[0].focus()
  }

  // TODO: this should update index correctly
  onClick($event:MouseEvent) {
    this.focus();
    $event.stopImmediatePropagation();
    $event.preventDefault();
  }

}