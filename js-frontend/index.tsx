import React from "react";
import { createRoot } from "react-dom/client";
import App from "./components/App";
import "./index.css";

const root = createRoot(document.getElementById("root") as Element);

root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
