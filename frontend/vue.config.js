const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
    publicPath: '.',
    productionSourceMap: false,
    css: {
        extract: false,
    },
    chainWebpack: (config) => {
        config.plugins.delete('prefetch')
        config.plugins.delete('preload')
    },
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
            },
        },
    },
})
