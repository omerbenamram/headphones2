import {
  it,
  inject,
  injectAsync,
  describe,
  beforeEachProviders,
  TestComponentBuilder
} from 'angular2/testing';

import {Component, provide} from 'angular2/core';

// Load the implementations that should be tested

describe("Hello World!", () => {
  beforeEach(() => {
    console.log("Testing!!!")
  });

  it('Should work', () => {
    expect(14).toEqual(14);
  })

});

import {HomeCmp} from './home.ts';

describe('HomeCmp', () => {
  beforeEachProviders(() => [
    HomeCmp
  ]);

  it('should fetch artists successfully', inject[HomeCmp], (home) => {
    spyOn(console, 'log');
    expect(console.log).not.toHaveBeenCalled();

    home.ngOnInit();
    expect(console.log).toHaveBeenCalled();
  })
});