import {Component, ViewEncapsulation} from '@angular/core';
import {Route, RouteConfig, ROUTER_DIRECTIVES} from '@angular/router-deprecated';

import {ArtistTableComponent} from './artist-table/artist-table.component.ts';
import {Navbar} from './navbar/navbar.component.ts';
//import {ManageCmp} from './manage/manage.component.ts';

// inject global css
require("font-awesome-webpack");
require("font-awesome-animation");

@Component({
  selector: 'app',
  directives: [Navbar, ROUTER_DIRECTIVES],
  template: `
  <navbar></navbar>
  <div class="container">
    <router-outlet></router-outlet>
  </div>
  `,
  styles: [require('./app.component.styl')],
  encapsulation: ViewEncapsulation.None,
})
@RouteConfig([
  new Route({path: '/', component: ArtistTableComponent, name: 'Home'}),
  //new Route({path: '/manage/...', component: ManageCmp, name: 'Manage'})
])
export class App {
}
