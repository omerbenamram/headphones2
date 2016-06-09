import {Component, ViewEncapsulation} from '@angular/core';
import {Route, RouteConfig, ROUTER_DIRECTIVES} from '@angular/router-deprecated';

import {MD_SIDENAV_DIRECTIVES} from '@angular2-material/sidenav';
import {MdIcon, MdIconRegistry} from '@angular2-material/icon';


import {ArtistTableComponent} from './artist-table/artist-table.component.ts';
import {Navbar} from './navbar/navbar.component.ts';
import {AppState} from "./app.service.ts";
import {MdToolbar} from "@angular2-material/toolbar/toolbar";
//import {ManageCmp} from './manage/manage.component.ts';

// inject global css
require("font-awesome-webpack");
require("font-awesome-animation");

@Component({
  selector: 'app',
  directives: [
    Navbar,
    ROUTER_DIRECTIVES,
    MD_SIDENAV_DIRECTIVES,
    MdToolbar,
    MD_SIDENAV_DIRECTIVES,
    MdIcon],
  template: require('./app.component.pug'),
  styles: [require('./app.component.styl')],
  providers: [MdIconRegistry],
  encapsulation: ViewEncapsulation.None,
})
@RouteConfig([
  new Route({path: '/', component: ArtistTableComponent, name: 'Home'}),
  //new Route({path: '/manage/...', component: ManageCmp, name: 'Manage'})
])
export class App {
  constructor(public appState:AppState) {

  }

  ngOnInit() {
    console.log('Initial App State', this.appState.state);
  }
}
