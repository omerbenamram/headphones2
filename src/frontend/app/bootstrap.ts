import 'reflect-metadata'
import {provide} from 'angular2/core';
import {bootstrap} from 'angular2/platform/browser';
import {ROUTER_PROVIDERS, LocationStrategy, HashLocationStrategy} from 'angular2/router';
//noinspection TypeScriptCheckImport
import {AppCmp} from './components/app/app';
import {HTTP_PROVIDERS} from "angular2/http";


document.addEventListener('DOMContentLoaded', function main() {
    bootstrap(AppCmp, [
        ...HTTP_PROVIDERS,
        ...ROUTER_PROVIDERS,
        provide(LocationStrategy, {useClass: HashLocationStrategy})]);
});
