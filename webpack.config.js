const path = require("path");

module.exports = {
    entry: "./js-frontend/index.tsx",
    output: {
        filename: "js-bundle.js",
        path: path.resolve(__dirname, "staticfiles/js")
    },
    mode: process.env.NODE_ENV || "development",
    module: {
        rules: [
            {
                test: /\.(js|ts)x?$/,
                exclude: /node_modules/,
                loader: "babel-loader",
                options: { presets: [ "@babel/preset-env", "@babel/preset-react" ] }
            },
            {
                test: /\.css$/i,
                use: ["style-loader", "css-loader", "postcss-loader"],
            },
        ]
    },
    resolve: {
        extensions: [ "", ".js", ".jsx", ".ts", ".tsx" ]
    }
};