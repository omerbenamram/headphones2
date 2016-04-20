/*
 * Providers provided by Angular
 */
import "reflect-metadata";
import "es6-shim";
import "jquery";
import "bootstrap-loader";
import "zone.js";
import "rxjs";

import "angular2/platform/browser";
import "angular2/platform/common_dom";
import "angular2/core";
import "angular2/common";
import "angular2/http";
import "angular2/router";

import {provide, enableProdMode} from "angular2/core";
import {bootstrap, ELEMENT_PROBE_PROVIDERS} from "angular2/platform/browser";
import {ROUTER_PROVIDERS, LocationStrategy, HashLocationStrategy} from "angular2/router";
import {HTTP_PROVIDERS} from "angular2/http";
import {AppCmp} from "./components/app/app.ts";

require('zone.js/dist/zone');
require('zone.js/dist/long-stack-trace-zone');


const ENV_PROVIDERS = [];

if ('production' === process.env.ENV) {
  enableProdMode();
} else {
  ENV_PROVIDERS.push(ELEMENT_PROBE_PROVIDERS);
}

document.addEventListener('DOMContentLoaded', function main() {
  //noinspection TypeScriptValidateTypes
  bootstrap(AppCmp, [
    ...ENV_PROVIDERS,
    ...HTTP_PROVIDERS,
    ...ROUTER_PROVIDERS,
    provide(LocationStrategy, {useClass: HashLocationStrategy})
  ])
    .catch(err => console.error(err));

});

// HMR
declare let module:any;

// activate hot module reload
//noinspection TypeScriptUnresolvedVariable,JSUnusedAssignment
if (module.hot) {

  // bootstrap must not be called after DOMContentLoaded,
  // otherwise it cannot be rerenderd after module replacement

  //noinspection TypeScriptValidateTypes
  bootstrap(AppCmp, [
    ...ENV_PROVIDERS,
    ...HTTP_PROVIDERS,
    ...ROUTER_PROVIDERS,
    provide(LocationStrategy, {useClass: HashLocationStrategy})
  ])
    .catch(err => console.error(err));

  //noinspection TypeScriptUnresolvedVariable,JSUnusedAssignment
  module.hot.accept();
}