/*
 * Providers provided by Angular
 */

//import 'core-js/es6';
import 'core-js/es6';
import 'core-js/es7/reflect';
require('zone.js/dist/zone');

// Typescript emit helpers polyfill
import 'ts-helpers';
//import "es6-shim";
import "jquery";
import "bootstrap-loader";
import "zone.js";
import "rxjs";

// Angular 2
import '@angular/platform-browser';
import '@angular/platform-browser-dynamic';
import '@angular/core';
import '@angular/common';
import '@angular/http';
import '@angular/router-deprecated';

// Material 2
import '@angular2-material/button';
import '@angular2-material/card';
import '@angular2-material/checkbox';
import '@angular2-material/grid-list';
import '@angular2-material/input';
import '@angular2-material/list';
import '@angular2-material/radio';
import '@angular2-material/progress-bar';
import '@angular2-material/progress-circle';
import '@angular2-material/sidenav';
import '@angular2-material/slide-toggle';
import '@angular2-material/tabs';
import '@angular2-material/toolbar';
// look in src/platform/angular2-material2 and src/platform/providers

import {enableProdMode} from "@angular/core";
import {bootstrap} from '@angular/platform-browser-dynamic';
import {ROUTER_PROVIDERS} from "@angular/router-deprecated";
import {HTTP_PROVIDERS} from "@angular/http";
import {App} from "./app/app.component.ts";

require('zone.js/dist/zone');
require('zone.js/dist/long-stack-trace-zone');

const ENV_PROVIDERS = [];

if ('production' === process.env.ENV) {
  enableProdMode();
}

export function main(initialHmrState?:any):Promise<any> {
  return bootstrap(App, [
    ...ENV_PROVIDERS,
    ...HTTP_PROVIDERS,
    ...ROUTER_PROVIDERS,
  ])
    .catch(err => console.error(err));
}
let ngHmr = require('angular2-hmr');
ngHmr.hotModuleReplacement(main, module);
