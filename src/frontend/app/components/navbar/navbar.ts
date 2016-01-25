import {Component} from 'angular2/core';
import {ROUTER_DIRECTIVES, Router, Location} from 'angular2/router';

@Component({
  selector: 'navbar',
  directives: [ROUTER_DIRECTIVES],
  template: `
      <nav id="headphones-navbar" class="navbar navbar-fixed-top">
       <div class="container-fluid">
         <div class="navbar-header">
          <i id="headphones-logo" class="nav-item navbar-brand fa fa-headphones faa-pulse animated-hover"></i>
          <span id="headphones-brand" class="nav-item navbar-brand" >Headphones 2</span>
         </div>
        <ul class="nav navbar-nav">
          <li class="divider-vertical"></li>
          <li class="active"><a href="#" class="nav-item nav-link" [routerLink]="['/Home']">Home</a></li>
          <li id="options-gear" class="active pull-right">
            <i href="#" class="fa fa-gear nav-item faa-spin animated-hover" [routerLink]="['/Manage/Home']"></i>
          </li>
        </ul>
       </div>
      </nav>
  `,
  styleUrls: [require('./navbar.styl')],
})
export class Navbar {
  constructor(public location:Location) {
  }
}
