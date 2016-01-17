import {Component} from 'angular2/core';
import {ROUTER_DIRECTIVES, Router, Location} from 'angular2/router';

@Component({
  selector: 'navbar',
  directives: [ROUTER_DIRECTIVES],
  template: `
      <nav id="headphones-navbar" class="navbar navbar-fixed-top">
       <div class="container-fluid">
         <div class="navbar-header">
          <i id="headphones-logo" class="nav-item navbar-brand fa fa-headphones"></i>
          <span id="headphones-brand" class="nav-item navbar-brand" >Headphones 2</span>
         </div>
        <ul class="nav navbar-nav">
          <li class="divider-vertical"></li>
          <li class="active"><a href="#" class="nav-item nav-link" [routerLink]="['/']">Home</a></li>
          <li class="active"><a href="#" class="nav-item nav-link">Test</a></li>
        </ul>
       </div>
      </nav>
  `,
  styleUrls: ['./components/navbar/navbar.css'],
})
export class Navbar {
  constructor(public location:Location) {
  }
}
