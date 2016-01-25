// Polyfills
import 'es6-shim';
// (these modules are what are in 'angular2/bundles/angular2-polyfills' so don't use that here)
import 'es6-promise';
import 'zone.js/lib/browser/zone-microtask';
require('es7-reflect-metadata/src/global/browser');
Error['stackTraceLimit'] = Infinity;
Zone['longStackTraceZone'] = require('zone.js/lib/zones/long-stack-trace.js');

// Angular 2
import 'angular2/platform/browser';
import 'angular2/platform/common_dom';
import 'angular2/router';
import 'angular2/http';
import 'angular2/core';

// RxJS
import 'rxjs';
