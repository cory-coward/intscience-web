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
                // exclude: /node_modules/,
                include: path.resolve(__dirname, "js-frontend"),
                use: ["style-loader", "css-loader", "postcss-loader"],
            },
            // {
            //     test: /\.(png|svg|jpg|gif)$/,
            //     exclude: /node_modules/,
            //     use: [
            //         {
            //             loader: "file-loader",
            //             options: {
            //                 name: "[name].[ext]",
            //             }
            //         },
            //     ]
            // },
        ]
    },
    resolve: {
        extensions: [ "", ".js", ".jsx", ".ts", ".tsx" ]
    }
};