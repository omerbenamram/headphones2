// Polyfills
import 'es6-shim';
// (these modules are what are in 'angular2/bundles/angular2-polyfills' so don't use that here)
import 'es6-promise';
import 'zone.js/lib/browser/zone-microtask';

import 'es7-reflect-metadata/src/global/browser';

// Angular 2
import 'angular2/platform/browser';
import 'angular2/platform/common_dom';
import 'angular2/router';
import 'angular2/http';
import 'angular2/core';

// RxJS
import 'rxjs';

//Bootstrap4
import 'jquery';
import 'bootstrap-loader';