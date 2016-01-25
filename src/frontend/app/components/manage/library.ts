import {Component} from "angular2/core";
import {COMMON_DIRECTIVES} from "angular2/common";
import {FORM_DIRECTIVES} from "angular2/common";
import {ManageService} from "../../services/manage/manage";
import {CORE_DIRECTIVES} from "angular2/common";
import {Configuration} from "../../interfaces/interfaces";
import {Observable} from "rxjs/Observable";
import {OnInit} from "angular2/core";

@Component({
  selector: 'manage-library',
  directives: [CORE_DIRECTIVES, COMMON_DIRECTIVES, FORM_DIRECTIVES],
  styles: [require('./library.styl')],
  template: `
  <div class="input-group">
    <h1>Library Path</h1>
    <input [(ngModel)]='libraryPath' type="text" class="form-control" placeholder="Enter Library Directory eg.(/home/User/music)">
    <div>{{(cachedConfiguration | async)?.MUSIC_LIBRARY_PATH}}</div>
  </div>
  `,
  viewProviders: [ManageService]
})
export class ManageLibraryCmp implements OnInit {

  cachedConfiguration:Observable<any>;

  constructor(private configurationSvc:ManageService) {
  }

  ngOnInit() {
    this.cachedConfiguration = this.configurationSvc.getConfiguration();
  }

}
