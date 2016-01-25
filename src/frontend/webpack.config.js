// @AngularClass

/*
 * Helper: root(), and rootDir() are defined at the bottom
 */
var sliceArgs = Function.prototype.call.bind(Array.prototype.slice);
var toString = Function.prototype.call.bind(Object.prototype.toString);
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

var rootAssetPath = './assets';

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
    // for faster builds use 'eval'
    metadata: metadata,
    devtool: 'source-map',
    debug: true,

    entry: {
        'vendor': './app/vendor.ts',
        'app': './app/bootstrap.ts' // our angular app
    },

    // Config for our build files
    output: {
        path: root('dist'),
        publicPath: 'assets',
        filename: '[name].bundle.js',
        sourceMapFilename: '[name].map',
        chunkFilename: '[id].chunk.js'
    },

    resolve: {
        // ensure loader extensions match
        extensions: ['', '.ts', '.js', '.json', '.css', '.html', '.styl']
    },

    module: {
        preLoaders: [{test: /\.ts$/, loader: 'tslint-loader'}],
        loaders: [
            // Support for .ts files.
            {
                test: /\.ts$/,
                loader: 'ts-loader',
                query: {
                    'ignoreDiagnostics': [
                        2403, // 2403 -> Subsequent variable declarations
                        2300, // 2300 Duplicate identifier
                        2374, // 2374 -> Duplicate number index signature
                        2375  // 2375 -> Duplicate string index signature
                    ]
                },
                exclude: [/\.spec\.ts$/, /\.e2e\.ts$/, /node_modules/, /tools/]
            },

            // Support for *.json files.
            {test: /\.json$/, loader: 'json-loader'},

            // Support for CSS as raw text
            {test: /\.css$/, loader: 'raw!postcss'},

            // support for .html as raw text
            {test: /\.html$/, loader: 'raw-loader'},
            {
                test: /\.styl$/,
                loaders: ['raw-loader', 'style-loader!css-loader!stylus-loader']
            },

            // Bootstrap 4
            {test: /bootstrap\/dist\/js\/umd\//, loader: 'imports?jQuery=jquery'}

        ],
        noParse: [
            /zone\.js\/dist\/.+/,
            /reflect-metadata/,
            /es(6|7)-.+/
        ]
    },

    plugins: [
        new webpack.optimize.OccurenceOrderPlugin(true),
        new CommonsChunkPlugin({name: 'vendor', filename: 'vendor.js', minChunks: Infinity}),
        new CommonsChunkPlugin({name: 'common', filename: 'common.js', minChunks: 2, chunks: ['app', 'vendor']}),
        new CopyWebpackPlugin([{from: 'app/assets', to: 'assets'}]),
        new HtmlWebpackPlugin({template: 'app/index.html', inject: true}),
        new ManifestRevisionPlugin(path.join('dist', 'manifest.json'), {
            rootAssetPath: rootAssetPath,
            ignorePaths: ['/styles', '/scripts']
        }),
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
    },
    // our Webpack Development Server config
    devServer: {
        historyApiFallback: true,
        contentBase: 'app/',
        publicPath: '/assets/'
    },
    node: {
        global: 'window',
        progress: false,
        crypto: 'empty',
        module: false,
        clearImmediate: false,
        setImmediate: false
    }
};

// Helper functions

//in python -> os.path.dirname(__file__)
function root(args) {
    args = sliceArgs(arguments, 0);
    return path.join.apply(path, [__dirname].concat(args));
}

function rootNode(args) {
    args = sliceArgs(arguments, 0);
    return root.apply(path, ['node_modules'].concat(args));
}
