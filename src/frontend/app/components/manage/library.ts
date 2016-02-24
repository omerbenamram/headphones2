import {Component, OnInit, Inject} from "angular2/core";
import {COMMON_DIRECTIVES, FORM_DIRECTIVES, CORE_DIRECTIVES, FormBuilder, Control, ControlGroup} from "angular2/common";
import {ManageService} from "../../services/manage/manage";
import {HeadphonesConfiguration} from "../../interfaces/interfaces";
import {Http} from "angular2/http";
import {ApiUrls} from "../../constsants/api"

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

    libraryPathValid(control:Control):Promise<ValidationResult> {
        return new Promise((resolve, reject) => {
            this._http.put(ApiUrls.ConfigurationAPI);
        })
    }


    ngOnInit() {
        this.configuration = this.configurationSvc.getConfiguration()
            .subscribe(res => this.configuration = res);
    }

}

interface ValidationResult {
    [key: string]:boolean;
}
