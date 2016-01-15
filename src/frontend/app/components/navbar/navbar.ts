import {Component} from 'angular2/core';
import {ROUTER_DIRECTIVES, Router, Location} from 'angular2/router';

@Component({
  selector: 'navbar',
  directives: [ROUTER_DIRECTIVES],
  template: `
      <nav id="headphones-navbar" class="navbar navbar-fixed-top">
       <div class="container-fluid">
         <div class="navbar-header">
          <i id="headphones-logo" class="navbar-brand fa fa-3x fa-headphones"></i>
          <h1 class="navbar-brand">Headphones 2</h1>
          <a class="navbar-link"  [routerLink]="['/']">Home</a>
        </div>
       </div>
      </nav>
  `,
  styleUrls: ['./components/navbar/navbar.css'],
})
export class Navbar {
  constructor(public location:Location) {
  }
}
