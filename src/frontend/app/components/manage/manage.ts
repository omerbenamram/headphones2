import {Component} from "angular2/core";
import {CORE_DIRECTIVES, FORM_DIRECTIVES, COMMON_DIRECTIVES} from "angular2/common";
import {ManageSidebar} from "./sidebar.ts";
import {Route, ROUTER_DIRECTIVES, RouteConfig} from "angular2/router";
import {ManageLibraryCmp} from "./library.ts";
import {ManageHomeCmp} from "./manage_home.ts";


@Component({
  selector: 'manage-app',
  directives: [ROUTER_DIRECTIVES, ManageSidebar, CORE_DIRECTIVES, FORM_DIRECTIVES, COMMON_DIRECTIVES],
  template: `
  <manage-sidebar></manage-sidebar>
  <div id="contents-container" class="container">
    <router-outlet></router-outlet>
  </div>
  `,
  styles: [require('./manage.styl')]
})
@RouteConfig([
  new Route({path: '/', component: ManageHomeCmp, name: 'Home'}),
  new Route({path: '/library', component: ManageLibraryCmp, name: 'Library'})
])
export class ManageCmp {
  constructor() {
  };
}
