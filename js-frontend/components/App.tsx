import React from "react";
import { Routes, Route } from "react-router-dom";
import CurrentWellReadings from "./CurrentWellReadings";
import Layout from "./Layout";

export default function App() {
    return (
        <Routes>
            <Route element={<Layout />}>
                <Route path="/current-well-readings" element={<CurrentWellReadings />} />
            </Route>
        </Routes>
    )
}