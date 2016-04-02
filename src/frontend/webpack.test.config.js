var helpers = require('./helpers.js');
var webpack = require('webpack');

const autoprefixer = require('autoprefixer');
var ProvidePlugin = require('webpack/lib/ProvidePlugin');

var rootAssetPath = helpers.root('app', 'assets');

var metadata = {
  title: 'Headphones 2',
  baseUrl: '/',
  host: 'localhost',
  port: 3000,
  ENV: 'development'
};

/*
 * Config
 */
module.exports = {
  metadata: metadata,
  devtool: 'eval-source-map',
  debug: true,

  entry: {
    'app': './app/bootstrap.ts' // our angular app
  },


  // Config for our build files
  output: {
    path: helpers.root('dist'),
    filename: '[name].bundle.js',
    sourceMapFilename: '[name].map',
    chunkFilename: '[id].chunk.js'
  },

  resolve: {
    modulesDirectories: ['node_modules'],
    // ensure loader extensions match
    alias: {
      'font-awesome-animation': helpers.root('app', 'assets', 'css', 'font-awesome-animation.min.css'),
    }
  },

  module: {
    preLoaders: [
      {test: /\.ts$/, loader: 'tslint-loader', exclude: [helpers.root('node_modules')]},
      {test: /\.js$/, loader: "source-map-loader", exclude: [helpers.root('node_modules/rxjs')]}
    ],
    loaders: [
      // Support for .ts files.
      {
        test: /\.ts$/,
        loader: 'awesome-typescript',
        query: {"compilerOptions": {"removeComments": true}},
        exclude: [/\.e2e\.ts$/]
      },

      // Support for *.json files.
      {test: /\.json$/, loader: 'json'},

      //css
      {test: /\.css$/, exclude: /\.useable\.css$/, loader: "style!css"},

      //jade
      {test: /\.jade$/, loader: "raw!jade-html"},

      // support for .html as raw text
      {test: /\.html$/, loader: 'raw'},

      // stylus should be served to angular as raw text
      {test: /\.styl$/, loader: 'raw!stylus'},

      // Bootstrap 4
      {test: /\.scss$/, loaders: ['style', 'css', 'postcss', 'sass']},
      {test: /bootstrap\/dist\/js\/umd\//, loader: 'imports?jQuery=jquery'},
      {test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=application/font-woff'},
      {test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=application/octet-stream'},
      {test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: 'file'},
      {test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=image/svg+xml'},

      {
        test: /\.(jpe?g|png|gif|svg([\?]?.*))$/i,
        loaders: [
          'file?context=' + rootAssetPath + '&name=[path][name].[hash].[ext]',
          'image-webpack?bypassOnDebug&optimizationLevel=7&interlaced=false'
        ]
      }
    ],
    noParse: [
      /zone\.js\/dist\/.+/,
      /reflect-metadata/,
      /es(6|7)-.+/,
      /angular2\/bundles\/.+/]
  },

  postcss: [autoprefixer],

  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        'ENV': JSON.stringify(metadata.ENV),
        'NODE_ENV': JSON.stringify(metadata.ENV)
      }
    }),
    //jQuery support for bootstrap
    new ProvidePlugin({
      jQuery: 'jquery',
      $: 'jquery',
      jquery: 'jquery',
      "Tether": 'tether',
      "window.Tether": "tether"
    })
  ],
  // Other module loader config
  tslint: {
    emitErrors: false,
    failOnHint: false,
    resourcePath: 'app'
  },
  // our Webpack Development Server config
  devServer: {
    port: metadata.port,
    contentBase: 'dist/',
    hot: true,
    // use python backend
    proxy: {
      '/api/*': {
        target: 'http://localhost:5000',
        secure: false
      }
    }
  },
  // we need this due to problems with es6-shim
  node: {
    global: 'window',
    progress: false,
    crypto: 'empty',
    module: false,
    clearImmediate: false,
    setImmediate: false
  }
};