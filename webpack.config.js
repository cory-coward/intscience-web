const path = require("path");

module.exports = {
    entry: "./js-frontend/index.js",
    output: {
        filename: "js-bundle.js",
        path: path.resolve(__dirname, "./staticfiles/js")
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx|ts|tsx)$/,
                exclude: /node_modules/,
                loader: "babel-loader",
                options: { presets: [ "@babel/preset-env", "@babel/preset-react" ] }
            }
        ]
    },
    resolve: {
        extensions: [ "", ".js", ".jsx" ]
    }
};