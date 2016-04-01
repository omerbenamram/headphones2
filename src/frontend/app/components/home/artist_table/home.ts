import {Component, OnInit} from 'angular2/core';
import {ArtistService} from '../../../services/artists/artists.ts';
import {CORE_DIRECTIVES, FORM_DIRECTIVES, NgStyle, NgClass} from 'angular2/common';
import {COMMON_DIRECTIVES} from 'angular2/common';
import {ArtworkService} from '../../../services/artwork/artwork.ts';
import {Artist} from "../../../interfaces/interfaces.ts";
import {ParseDatePipe} from "../../../pipes/parse_date.ts";

@Component({
    selector: 'home',
    directives: [CORE_DIRECTIVES, FORM_DIRECTIVES, COMMON_DIRECTIVES, NgClass, NgStyle],
    template: require('./home.jade'),
    styles: [require('./home.styl')],
    pipes: [ParseDatePipe],
    viewProviders: [ArtistService, ArtworkService]
})
export class HomeCmp implements OnInit {
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
