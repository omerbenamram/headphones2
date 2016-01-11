import {ArtistService} from './artists.ts';
import {Inject} from "angular2/core";

// TODO: this is not working! (learn how to test :))
export function main(@Inject ArtistService) {
  describe('Artist Service', () => {
    let artists = [];

    it('should return the list of names', () => {
      artists = ArtistService.getArtists();
      expect(artists).toEqual(jasmine.any(Array));
    });
  });
}
