import {Component, ViewEncapsulation} from 'angular2/core';
import {RouteConfig, ROUTER_DIRECTIVES} from 'angular2/router';
// import {HTTP_PROVIDERS} from 'angular2/http';

import {HomeCmp} from '../home/home';
import {Navbar} from "../navbar/navbar";


@Component({
  selector: 'app',
  directives: [Navbar, ROUTER_DIRECTIVES],
  template:`
  <navbar></navbar>
  <div class="container">
    <router-outlet></router-outlet>
  </div>
  `,
  styleUrls: ['./components/app/app.css'],
  encapsulation: ViewEncapsulation.None,
})
@RouteConfig([
  {path: '/', component: HomeCmp, as: 'Home'},
])
export class AppCmp {
}
