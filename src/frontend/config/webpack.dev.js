var helpers = require('./helpers.js');
var webpack = require('webpack');

/**
 * Webpack Plugins
 */


// Webpack Plugins
var CommonsChunkPlugin = webpack.optimize.CommonsChunkPlugin;
var CopyWebpackPlugin = require('copy-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var ForkCheckerPlugin = require('awesome-typescript-loader').ForkCheckerPlugin;

const autoprefixer = require('autoprefixer');
var ProvidePlugin = require('webpack/lib/ProvidePlugin');
const DefinePlugin = require('webpack/lib/DefinePlugin');


var rootAssetPath = helpers.root('src', 'assets');

const ENV = process.env.ENV = process.env.NODE_ENV = 'development';
const HMR = helpers.hasProcessFlag('hot');

var METADATA = {
  title: 'Headphones 2',
  baseUrl: '/',
  host: 'localhost',
  port: 3000,
  ENV: ENV,
  HMR: HMR
};

/*
 * Config
 */
module.exports = {
  metadata: METADATA,
  devtool: 'cheap-module-eval-source-map',
  debug: true,

  entry: {
    'polyfills': './src/polyfills.ts',
    'vendor': './src/vendor.ts',
    'main': './src/main.browser.ts',
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
      'font-awesome-animation': helpers.root('src', 'assets', 'css', 'font-awesome-animation.min.css'),
    }
  },

  module: {
    preLoaders: [
      {test: /\.js$/, loader: "source-map-loader", exclude: [helpers.root('node_modules/rxjs')]}
    ],
    loaders: [
      // Support for .ts files.
      {test: /\.ts$/, loader: 'awesome-typescript', exclude: [/\.(spec|e2e|async)\.ts$/]},

      // Support for *.json files.
      {test: /\.json$/, loader: 'json'},

      //css
      {test: /\.css$/, exclude: /\.useable\.css$/, loader: "style!css"},

      //jade
      {test: /\.jade$/, loader: "raw!jade-html"},
      {test: /\.pug$/, loader: "raw!jade-html"},

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
      /reflect-METADATA/,
      /es(6|7)-.+/,
      /angular2\/bundles\/.+/]
  },

  postcss: [autoprefixer],

  plugins: [
    new ForkCheckerPlugin(),
    new CopyWebpackPlugin([{from: 'src/assets', to: 'assets'}]),
    new HtmlWebpackPlugin({template: 'src/index.html', inject: true}),
    new DefinePlugin({
      'ENV': JSON.stringify(METADATA.ENV),
      'HMR': METADATA.HMR,
      'process.env': {
        'ENV': JSON.stringify(METADATA.ENV),
        'NODE_ENV': JSON.stringify(METADATA.ENV),
        'HMR': METADATA.HMR
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
    resourcePath: 'src'
  },
  // our Webpack Development Server config
  devServer: {
    port: METADATA.port,
    contentBase: 'dist/',
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