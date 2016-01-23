import {Component} from 'angular2/core';
import {CORE_DIRECTIVES, FORM_DIRECTIVES, COMMON_DIRECTIVES} from 'angular2/common';
import {ROUTER_DIRECTIVES} from "angular2/router";
import {NgClass} from "angular2/common";
import {RouteData} from "angular2/router";
import {RouteParams} from "angular2/router";
import {Route} from "angular2/router";
import {ROUTER_PROVIDERS} from "angular2/router";


@Component({
  selector: 'manage-sidebar',
  directives: [CORE_DIRECTIVES, COMMON_DIRECTIVES, ROUTER_DIRECTIVES, NgClass],
  styleUrls: ['./components/manage/sidebar.css'],
  template: `
  <div id="sidebar-wrapper">
      <ul id="sidebar-nav" class="nav nav-sidebar">
         <li>
          <div>
            <span class="fa fa-music sidebar-icon"></span>
            <a [routerLink]="['/Manage/Library']">Library</a>
          </div>
         </li>
         <hr>
         <li>
          <div>
            <span class="fa fa-cog sidebar-icon"></span>
            <a [routerLink]="['/Manage/Library']">Another Item</a>
          </div>
         </li>
         <hr>
      </ul>
  </div>
  `
})
export class ManageSidebar {
  constructor() {
  };
}
