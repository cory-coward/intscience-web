const path = require("path");

module.exports = {
    entry: "./js-frontend/index.js",
    output: {
        filename: "js-bundle.js",
        path: path.resolve(__dirname, "staticfiles/js")
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx|ts|tsx)$/,
                exclude: /node_modules/,
                loader: "babel-loader",
                options: { presets: [ "@babel/preset-env", "@babel/preset-react" ] }
            },
            {
                test: /\.css$/i,
                include: path.resolve(__dirname, "js-frontend"),
                use: [ "style-loader", "css-loader", "postcss-loader" ]
            }
        ]
    },
    resolve: {
        extensions: [ "", ".js", ".jsx" ]
    }
};