import {Component} from "angular2/core";
import {ROUTER_DIRECTIVES, Location} from "angular2/router";
import {SearchComponent} from "./search/search.ts";

@Component({
  selector: 'navbar',
  directives: [ROUTER_DIRECTIVES, SearchComponent],
  template: require('./navbar.jade'),
  styles: [require('./navbar.styl')],
})
export class Navbar {
  constructor(public location:Location) {
  }
}
