// Polyfills
import 'es6-shim';
import 'es6-promise';
import 'zone.js';
import 'reflect-metadata';
require('es7-reflect-metadata/src/global/browser');

// (these modules are what are in 'angular2/bundles/angular2-polyfills' so don't use that here)
// In production Reflect with es7-reflect-metadata/reflect-metadata is added

// by webpack.prod.config ProvidePlugin
Error['stackTraceLimit'] = Infinity;
require('zone.js/dist/zone-microtask');
require('zone.js/dist/long-stack-trace-zone');

// RxJS
// In development we are including every operator
require('rxjs/add/operator/map');
require('rxjs/add/operator/mergeMap');

//Bootstrap4
import 'jquery';
import 'bootstrap-loader';