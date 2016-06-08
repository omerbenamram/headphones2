import {Component} from "@angular/core";
import {ROUTER_DIRECTIVES} from "@angular/router-deprecated";
import {SearchComponent} from "./search.component.ts";

@Component({
  selector: 'navbar',
  directives: [ROUTER_DIRECTIVES, SearchComponent],
  template: require('./navbar.component.pug'),
  styles: [require('./navbar.component.styl')],
})
export class Navbar {
  constructor() {
  }
}
