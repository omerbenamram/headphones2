import {join} from 'path';
import {APP_SRC, APP_DEST} from '../config';

var jade = require('jade');

export = function buildJadeDev(gulp, plugins, option) {
  return function () {
    return gulp.src(join(APP_SRC, '**', '*.jade'))
      .pipe(plugins.jade({
        jade: jade,
        pretty: true
      }))
      .pipe(gulp.dest(APP_DEST));
  };
}
