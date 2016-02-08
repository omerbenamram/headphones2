var sliceArgs = Function.prototype.call.bind(Array.prototype.slice);
var path = require('path');
var webpack = require('webpack');
var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');
var CopyWebpackPlugin = require('copy-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var ExtractTextPlugin = require("extract-text-webpack-plugin");

const autoprefixer = require('autoprefixer');
var ProvidePlugin = require('webpack/lib/ProvidePlugin');

// Webpack Plugins
var CommonsChunkPlugin = webpack.optimize.CommonsChunkPlugin;

var rootAssetPath = './app/assets';

var metadata = {
    title: 'Headphones 2',
    baseUrl: '/',
    host: 'localhost',
    port: 8080,
    ENV: 'development'
};

/*
 * Config
 */
module.exports = {
    // for faster builds use 'eval'
    metadata: metadata,
    devtool: 'eval-source-map',
    debug: true,

    entry: {
        'vendor': './app/vendor.ts', // various imports
        'app': ['webpack/hot/dev-server', './app/bootstrap.ts'] // our angular app
    },


    // Config for our build files
    output: {
        path: root('dist'),
        filename: '[name].bundle.js',
        sourceMapFilename: '[name].map',
        chunkFilename: '[id].chunk.js'
    },

    // our Webpack Development Server config
    devServer: {
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

    resolve: {
        modulesDirectories: ['node_modules'],
        // ensure loader extensions match
        extensions: ['', '.ts', '.js', '.json', '.css', '.html', '.styl'],
        alias: {
            'font-awesome-animation' : root('app','assets','css','font-awesome-animation.min.css'),
        }
    },

    module: {
        preLoaders: [
            // { test: /\.ts$/, loader: 'tslint-loader', exclude: [ root('node_modules') ] },
            // TODO(gdi2290): `exclude: [ root('node_modules/rxjs') ]` fixed with rxjs 5 beta.2 release
            {test: /\.js$/, loader: "source-map-loader", exclude: [root('node_modules/rxjs')]}
        ],
        loaders: [
            // Support Angular 2 async routes via .async.ts
            {test: /\.async\.ts$/, loaders: ['es6-promise-loader', 'ts-loader'], exclude: [/\.(spec|e2e)\.ts$/]},

            // Support for .ts files.
            {test: /\.ts$/, loader: 'ts-loader', exclude: [/\.(spec|e2e|async)\.ts$/]},

            // Support for *.json files.
            {test: /\.json$/, loader: 'json-loader'},

            //css
            {test: /\.css$/, exclude: /\.useable\.css$/, loader: "style-loader!css-loader"},

            //jade
            {test: /\.jade$/, loader: "raw-loader!jade-html"},

            // support for .html as raw text
            {test: /\.html$/, loader: 'raw-loader'},

            // stylus should be served to angular as raw text
            {test: /\.styl$/, loader: 'raw-loader!stylus-loader'},

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

    // sassResources: path.resolve(__dirname, "./node_modules/bootstrap/scss"),
    postcss: [autoprefixer],

    plugins: [
        new webpack.optimize.OccurenceOrderPlugin(true),
        new CommonsChunkPlugin({name: 'vendor', filename: 'vendor.js', minChunks: Infinity}),
        new CommonsChunkPlugin({name: 'common', filename: 'common.js', minChunks: 2, chunks: ['app', 'vendor']}),
        new CopyWebpackPlugin([{from: 'app/assets', to: 'assets'}]),
        new ExtractTextPlugin("external_styles.css"),
        new HtmlWebpackPlugin({template: 'app/index.html', inject: true}),
        new ManifestRevisionPlugin(path.join('dist', 'manifest.json'), {
            rootAssetPath: rootAssetPath,
            ignorePaths: ['/css']
        }),
        //jQuery support for bootstrap
        new ProvidePlugin({
            jQuery: 'jquery',
            $: 'jquery',
            jquery: 'jquery'
        })

    ],

    // Other module loader config
    tslint: {
        emitErrors: false,
        failOnHint: false
    }

};

// Helper functions

//in python -> os.path.dirname(__file__)
function root(args) {
    args = sliceArgs(arguments, 0);
    return path.join.apply(path, [__dirname].concat(args));
}