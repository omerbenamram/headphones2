/*
 * Providers provided by Angular
 */
import 'zone.js';
import 'reflect-metadata';
import 'jquery';
import 'bootstrap-loader';

import {provide, enableProdMode} from 'angular2/core';
import {bootstrap, ELEMENT_PROBE_PROVIDERS} from 'angular2/platform/browser';
import {ROUTER_PROVIDERS, LocationStrategy, HashLocationStrategy} from 'angular2/router';
import {HTTP_PROVIDERS} from 'angular2/http';

const ENV_PROVIDERS = [];

if ('production' === process.env.ENV) {
  enableProdMode();
} else {
  ENV_PROVIDERS.push(ELEMENT_PROBE_PROVIDERS);
}

/*
 * App Component
 * our top level component that holds all of our components
 */
import {AppCmp} from './components/app/App';

/*
 * Bootstrap our Angular app with a top level component `App` and inject
 * our Services and Providers into Angular's dependency injection
 */

document.addEventListener('DOMContentLoaded', function main() {
  bootstrap(AppCmp, [
    ...ENV_PROVIDERS,
    ...HTTP_PROVIDERS,
    ...ROUTER_PROVIDERS,
    provide(LocationStrategy, { useClass: HashLocationStrategy })
  ])
  .catch(err => console.error(err));

});


/*
 * Modified for using hot module reload
 */

// typescript lint error 'Cannot find name "module"' fix
declare let module: any;

// activate hot module reload
if (module.hot) {

  // bootstrap must not be called after DOMContentLoaded,
  // otherwise it cannot be rerenderd after module replacement
  
  bootstrap(AppCmp, [
      ...ENV_PROVIDERS,
      ...HTTP_PROVIDERS,
      ...ROUTER_PROVIDERS,
      provide(LocationStrategy, { useClass: HashLocationStrategy })
    ])
    .catch(err => console.error(err));

  module.hot.accept();
}