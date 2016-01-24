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

// Webpack Plugins
var CommonsChunkPlugin = webpack.optimize.CommonsChunkPlugin;

var rootAssetPath = './assets';

/*
 * Config
 */
module.exports = {
    // for faster builds use 'eval'
    devtool: 'source-map',
    debug: true,

    entry: {
        'vendor': './app/vendor.ts',
        'app': './app/bootstrap.ts' // our angular app
    },

    // Config for our build files
    output: {
        path: root('dist'),
        publicPath: 'http://localhost:2992/assets',
        filename: '[name].[chunkhash].js',
        chunkFilename: '[id].[chunkhash].js'
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
            {test: /\.css$/, loader: 'raw-loader'},

            // support for .html as raw text
            {test: /\.html$/, loader: 'raw-loader'},

            {test: /\.styl$/, loader: 'style-loader!css-loader!stylus-loader'}


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
        new ManifestRevisionPlugin(path.join('dist', 'manifest.json'), {
            rootAssetPath: rootAssetPath,
            ignorePaths: ['/styles', '/scripts']
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
