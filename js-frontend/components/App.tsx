import React from "react";
import { Routes, Route } from "react-router-dom";
import { Slide, ToastContainer} from "react-toastify";
import { injectStyle } from "react-toastify/dist/inject-style";
import CurrentWellReadings from "./CurrentWellReadings";
import Layout from "./Layout";

if (typeof window !== "undefined") {
    injectStyle();
}

export default function App() {
    return (
        <>
            <ToastContainer
                position="bottom-right"
                theme="dark"
                transition={Slide}
                pauseOnHover={false}
                pauseOnFocusLoss={false}
            />
            <Routes>
                <Route element={<Layout />}>
                    <Route path="/current-well-readings" element={<CurrentWellReadings />} />
                </Route>
            </Routes>
        </>
    )
}