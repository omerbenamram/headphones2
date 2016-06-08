import {Pipe, PipeTransform} from "@angular/core";
@Pipe({
  name: 'parseDate'
})
export class ParseDatePipe implements PipeTransform {
  transform(date):number {
    return Date.parse(date);
  }
}