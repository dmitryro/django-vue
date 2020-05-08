const fs = require('fs');
const path = require('path');
const HOST = '0.0.0.0';
const PORT = 8080


module.exports = config => {
  config.devServer = {
    compress: true,	  
    host: HOST,
    port: PORT,
    open: true,
    clientLogLevel: 'warning',
    hot: true,
    contentBase: 'dist',
    compress: true,
    host: HOST,
    port: PORT,
    open: true,
    overlay: { warnings: false, errors: true },
    publicPath: '/',
    quiet: true
  };
}
