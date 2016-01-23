import {Component} from 'angular2/core';
import {CORE_DIRECTIVES, FORM_DIRECTIVES, COMMON_DIRECTIVES} from 'angular2/common';
import {ManageSidebar} from "./sidebar";
import {Route} from "angular2/router";
import {ROUTER_DIRECTIVES} from "angular2/router";
import {RouteConfig} from "angular2/router";
import {ManageLibraryCmp} from "./library";
import {ManageHomeCmp} from "./manage_home";


@Component({
  selector: 'manage-app',
  directives: [ROUTER_DIRECTIVES, ManageSidebar, CORE_DIRECTIVES, FORM_DIRECTIVES, COMMON_DIRECTIVES],
  template: `
  <manage-sidebar></manage-sidebar>
  <div class="container">
    <router-outlet></router-outlet>
  </div>
  `,
})
@RouteConfig([
  new Route({path: '/', component: ManageHomeCmp, name:'Home'}),
  new Route({path: '/library', component: ManageLibraryCmp, name:'Library'})
])
export class ManageCmp{
  constructor() {};
}
