import 'reflect-metadata'
import {provide} from 'angular2/core';
import {bootstrap} from 'angular2/platform/browser';
import {ROUTER_PROVIDERS, LocationStrategy, HashLocationStrategy} from 'angular2/router';
//noinspection TypeScriptCheckImport
import {AppCmp} from './components/app/app';
import {HTTP_PROVIDERS} from "angular2/http";

import {AppViewListener} from 'angular2/src/core/linker/view_listener';
import {DebugElementViewListener, inspectNativeElement} from 'angular2/platform/common_dom';
import {bind} from 'angular2/core';


document.addEventListener('DOMContentLoaded', function main() {
    bootstrap(AppCmp, [
        ...HTTP_PROVIDERS,
        ...ROUTER_PROVIDERS,
        provide(LocationStrategy, {useClass: HashLocationStrategy}),
        bind(AppViewListener).toClass(DebugElementViewListener)
    ])
        .catch(err => console.error(err))
        .then(applicationReference => {
            const w:any = window;
            w.ng.probe = inspectNativeElement;
        })
});
