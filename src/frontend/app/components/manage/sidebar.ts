import {Component} from "angular2/core";
import {CORE_DIRECTIVES, COMMON_DIRECTIVES} from "angular2/common";
import {ROUTER_DIRECTIVES} from "angular2/router";

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
