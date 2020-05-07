var path = require('path')
var utils = require('./utils')
var multiPage = require('./multi-page')
var config = require('../config')
var webpack = require('webpack')
const {VueLoaderPlugin} = require('vue-loader');
var appConfig = require('../config/app-config')
const ThemeColorReplacer = require('webpack-theme-color-replacer')
const forElementUI = require('webpack-theme-color-replacer/forElementUI')
const JoinFileContentPlugin = require('join-file-content-plugin')

function resolve(dir) {
    return path.join(__dirname, '..', dir)
}

// Main const. Feel free to change it
const PATHS = {
  src: path.join(__dirname, "../src"),
  dist: path.join(__dirname, "../dist"),
  assets: "assets/"
};

module.exports = {
    externals: {
      paths: PATHS,
      Vue: 'vue'
    },
    entry: multiPage.getEntryPages(),
    output: {
        path: config.build.assetsRoot,
        filename: '[name].js',
        publicPath: config.isBuild
            ? config.build.assetsPublicPath
            : config.dev.assetsPublicPath,
    },
    resolve: {
        extensions: ['.js', '.vue', '.json', 'jsx', 'styl', 'tsx'],
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
            '@': resolve('src')
        }
    },
    module: {
        rules: [
            /*{
              test: /\.(js|vue)$/,
              loader: 'eslint-loader',
              enforce: 'pre',
              include: [resolve('src'), resolve('test')],
              options: {
                formatter: require('eslint-friendly-formatter')
              }
            },*/
            { test: /\.styl$/, loader: 'style-loader!css-loader!stylus-loader' },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {}
            },
            {
                test: /\.js$/,
                include: [resolve('src'), resolve('test')],
                use: [
                    //step-2
                    'babel-loader?cacheDirectory',
                    //step-1
                    {
                        loader: 'js-conditional-compile-loader',
                        options: {
                            isDebug: process.env.NODE_ENV === 'development', // optional, this expression is default
                            envTest: process.env.ENV_CONFIG === 'test',  // any name you want, used for /* IFTRUE_evnTest ...js code... FITRUE_evnTest */
                            isPreview: process.env.npm_config_preview, // npm run build-demo --preview, for mock client data
                        }
                    },
                ],
            },
            {
                test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
                loader: 'url-loader',
                options: {
                    limit: 10000,
                    name: utils.assetsPath('img/[name].[hash:7].[ext]')
                }
            },
            {
                test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
                loader: 'url-loader',
                options: {
                    limit: 10000,
                    name: utils.assetsPath('font/[name].[hash:7].[ext]')
                }
            }
        ]
    },
    plugins: [
        new VueLoaderPlugin(),
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: JSON.stringify(process.env.NODE_ENV),
                ENV_CONFIG: JSON.stringify(process.env.ENV_CONFIG),
            }
        }),
        new JoinFileContentPlugin({
            file: 'node_modules/element-theme-chalk/src/common/var.scss',
            prependFile: 'src/css/element-theme/theme-changed.scss'
        }),
        new ThemeColorReplacer({
            fileName: 'css/theme-colors.[contenthash:8].css',
            matchColors: [
                ...forElementUI.getElementUISeries(appConfig.themeColor),  //element-ui
                '#0cdd3a',  
                '#c655dd',
            ],
            changeSelector: forElementUI.changeSelector,
            isJsUgly: config.isBuild,
            // injectCss: false,
            // resolveCss(resultCss) { // optional. Resolve result css code as you wish.
            //     return resultCss + youCssCode
            // }
        })
    ],

    node: {
        // prevent webpack from injecting useless setImmediate polyfill because Vue
        // source contains it (although only uses it if it's native).
        setImmediate: false,
        // prevent webpack from injecting mocks to Node native modules
        // that does not make sense for the client
        dgram: 'empty',
        fs: 'empty',
        net: 'empty',
        tls: 'empty',
        child_process: 'empty'
    }
}
