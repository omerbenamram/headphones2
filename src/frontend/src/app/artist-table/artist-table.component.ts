import {Component, OnInit} from "@angular/core";
import {CORE_DIRECTIVES, FORM_DIRECTIVES, NgStyle, NgClass, COMMON_DIRECTIVES} from "@angular/common";
import {
  ArtistService,
  ArtworkService,
  Artist,
  ParseDatePipe
} from '../shared/index.ts';

@Component({
  selector: 'home',
  directives: [CORE_DIRECTIVES, FORM_DIRECTIVES, COMMON_DIRECTIVES, NgClass, NgStyle],
  template: require('./artist-table.component.pug'),
  styles: [require('./artist-table.component.styl')],
  pipes: [ParseDatePipe],
  viewProviders: [ArtistService, ArtworkService]
})
export class ArtistTableComponent implements OnInit {
  public artists:Artist[];

  ngOnInit() {
    this.artistSvc.getArtists().subscribe(
      (artists) => {
        artists.forEach((artist) => {
            // Fetch artwork for all artists
            this.artworkSvc.getArtworkUrl('artist', 'large', artist.id)
              .subscribe(
                (artworkUrl) => {
                  artist['imageUrl'] = artworkUrl
                },
                (err) => console.log(`Failed to fetch artwork for artist ${artist}`)
              );
          }
        );
        this.artists = artists;
      },
      (err) => console.log(err),
      () => {
      } // Done
    )
  }

  constructor(private artistSvc:ArtistService,
              private artworkSvc:ArtworkService) {
  }
}
