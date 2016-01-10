import {join} from 'path';
import {APP_SRC, APP_DEST} from '../config';

export = function(gulp, plugins) {
  return function() {
    return gulp.src(join(APP_SRC, '**', '*.styl'))
    .pipe(plugins.stylus())
    .pipe(gulp.dest(APP_DEST));
  };
}
