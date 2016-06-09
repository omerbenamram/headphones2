// App
export * from './app.component.ts';
export * from './app.service.ts'

import {AppState} from "./app.service.ts";

// Application wide providers
export const APP_PROVIDERS = [
  AppState
];
