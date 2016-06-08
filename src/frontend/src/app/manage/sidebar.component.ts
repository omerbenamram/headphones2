import {Component} from "@angular/core";
import {CORE_DIRECTIVES, COMMON_DIRECTIVES} from "@angular/common";
import {ROUTER_DIRECTIVES} from "@angular/router-deprecated";

@Component({
  selector: 'manage-sidebar',
  directives: [CORE_DIRECTIVES, COMMON_DIRECTIVES, ROUTER_DIRECTIVES],
  styles: [require('./sidebar.styl')],
  template: require('./sidebar.jade')
})
export class ManageSidebar {
  constructor() {
  };
}
