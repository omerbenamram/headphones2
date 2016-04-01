import {Pipe, PipeTransform} from "angular2/core";
@Pipe({
    name: 'parseDate'
})
export class ParseDatePipe implements PipeTransform {
    transform(date):number {
        return Date.parse(date);
    }
}