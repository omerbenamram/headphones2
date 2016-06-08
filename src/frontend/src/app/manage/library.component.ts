import {Component, OnInit} from "@angular/core";
import {COMMON_DIRECTIVES, FORM_DIRECTIVES, CORE_DIRECTIVES, FormBuilder, Control, ControlGroup} from "@angular/common";
import {ManageService} from "../../services/manage/manage.service.ts";
import {HeadphonesConfiguration} from "../../interfaces/interfaces.ts";

@Component({
  selector: 'manage-library',
  directives: [CORE_DIRECTIVES, COMMON_DIRECTIVES, FORM_DIRECTIVES],
  styles: [require('./library.styl')],
  template: require('./library.jade'),
  viewProviders: [ManageService]
})
export class ManageLibraryCmp implements OnInit {

  configuration:HeadphonesConfiguration = <HeadphonesConfiguration>{};
  
  libraryPathControl:Control;
  libraryForm:ControlGroup;


  constructor(private _configurationSvc:ManageService,
              private _formBuilder:FormBuilder) {
    this.libraryPathControl = new Control();

    this.libraryForm = _formBuilder.group({
      libraryPath: this.libraryPathControl
    });
  }

  updateConfiguration() {
    this._configurationSvc.updateConfiguration(this.configuration)
      .subscribe(
        success => {
        },
        error => console.log(error)
      )
  }

  ngOnInit() {
    this._configurationSvc.getConfiguration().subscribe((res) => {
      this.configuration = res
    });
  }

}