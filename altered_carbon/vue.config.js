module.exports = {
  lintOnSave: true,
  runtimeCompiler: true,
  configureWebpack: {
    entry: ['@babel/polyfill', './src/main.js'],
    plugins: [
    ],
    //Necessary to run npm link https://webpack.js.org/configuration/resolve/#resolve-symlinks
    resolve: {
      symlinks: false
    },
    devServer: {
      contentBase: 'localhost',
      port: 8080,
      host: '127.0.0.1'
    }
  },
  transpileDependencies: [
    '@coreui/utils'
  ]
};
