import {Component, OnInit, Inject} from "angular2/core";
import {COMMON_DIRECTIVES, FORM_DIRECTIVES, CORE_DIRECTIVES, FormBuilder, Control, ControlGroup} from "angular2/common";
import {ManageService} from "../../services/manage/manage.ts";
import {HeadphonesConfiguration} from "../../interfaces/interfaces.ts";
import {Http} from "angular2/http";

@Component({
  selector: 'manage-library',
  directives: [CORE_DIRECTIVES, COMMON_DIRECTIVES, FORM_DIRECTIVES],
  styles: [require('./library.styl')],
  template: require('./library.jade'),
  viewProviders: [ManageService]
})
export class ManageLibraryCmp implements OnInit {

  configuration = <HeadphonesConfiguration>{};
  libraryPath:Control;

  libraryForm:ControlGroup;


  constructor(@Inject(Http)
              private _http:Http,
              private configurationSvc:ManageService,
              private _formBuilder:FormBuilder) {
    this.libraryPath = new Control();

    this.libraryForm = _formBuilder.group({
      libraryPath: this.libraryPath
    });
  }

  updateConfiguration() {
    this.configurationSvc.updateConfiguration(this.configuration)
      .subscribe(
        success => {
        },
        error => console.log(error)
      )
  }

  ngOnInit() {
    this.configurationSvc.getConfiguration()
      .subscribe(res => this.configuration = res);
  }

}

interface ValidationResult {
  [key:string]:boolean;
}
