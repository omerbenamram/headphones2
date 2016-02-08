import {Component} from "angular2/core";
import {COMMON_DIRECTIVES} from "angular2/common";
import {FORM_DIRECTIVES} from "angular2/common";
import {ManageService} from "../../services/manage/manage";
import {CORE_DIRECTIVES} from "angular2/common";
import {HeadphonesConfiguration} from "../../interfaces/interfaces";
import {Observable} from "rxjs/Observable";
import {OnInit} from "angular2/core";

@Component({
  selector: 'manage-library',
  directives: [CORE_DIRECTIVES, COMMON_DIRECTIVES, FORM_DIRECTIVES],
  styles: [require('./library.styl')],
  template: require('./library.jade'),
  viewProviders: [ManageService]
})
export class ManageLibraryCmp implements OnInit {

  configuration = <HeadphonesConfiguration>{};

  constructor(private configurationSvc:ManageService) {
  }

  updateConfiguration() {
    this.configurationSvc.updateConfiguration(this.configuration);
  }

  ngOnInit() {
    this.configuration = this.configurationSvc.getConfiguration()
        .subscribe(res => this.configuration = res);
  }

}
