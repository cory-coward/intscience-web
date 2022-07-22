import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./components/App";
import "./index.css";

const root = createRoot(document.getElementById("root") as Element);

root.render(
    <React.StrictMode>
        <BrowserRouter basename="/dashboard/">
            <App />
        </BrowserRouter>
    </React.StrictMode>
);
