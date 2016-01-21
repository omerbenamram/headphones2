import {Component, ViewEncapsulation} from 'angular2/core';
import {Route, RouteConfig, ROUTER_DIRECTIVES} from 'angular2/router';

import {HomeCmp} from '../home/home';
import {Navbar} from '../navbar/navbar';


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
  new Route({path: '/', component: HomeCmp, name: 'Home'})
])
export class AppCmp {
}
