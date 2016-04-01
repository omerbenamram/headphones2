import {Component, ViewEncapsulation} from 'angular2/core';
import {Route, RouteConfig, ROUTER_DIRECTIVES} from 'angular2/router';

import {HomeCmp} from '../home/artist_table/home.ts';
import {Navbar} from '../navbar/navbar.ts';
import {ManageCmp} from "../manage/manage.ts";

// inject global css
require("font-awesome-webpack");
require("font-awesome-animation");

@Component({
  selector: 'app',
  directives: [Navbar, ROUTER_DIRECTIVES],
  template:`
  <navbar></navbar>
  <div class="container">
    <router-outlet></router-outlet>
  </div>
  `,
  styles: [require('./app.styl')],
  encapsulation: ViewEncapsulation.None,
})
@RouteConfig([
  new Route({path: '/', component: HomeCmp, name: 'Home'}),
  new Route({path: '/manage/...', component: ManageCmp, name: 'Manage'})
])
export class AppCmp {
}
