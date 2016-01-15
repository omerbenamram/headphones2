import {Component, ViewEncapsulation} from 'angular2/core';
import {RouteConfig, ROUTER_DIRECTIVES} from 'angular2/router';
// import {HTTP_PROVIDERS} from 'angular2/http';

import {HomeCmp} from '../home/home';

@Component({
  selector: 'app',
  template:`
  <div class="container">
  <router-outlet></router-outlet>
  </div>
  `,
  styleUrls: ['./components/app/app.css'],
  encapsulation: ViewEncapsulation.None,
  directives: [ROUTER_DIRECTIVES]
})
@RouteConfig([
  {path: '/', component: HomeCmp, as: 'Home'},
])
export class AppCmp {
}
