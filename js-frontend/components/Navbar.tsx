import React from "react";
import { NavLink } from "react-router-dom";

export default function Navbar() {
    return (
        <div className="mb-6 px-10 bg-gray-800 space-x-6">
            <NavLink
                to="/current-well-readings"
                className={({ isActive }) => (isActive ? "active-navlink" : "navlink")}
            >
                Current Well Readings
            </NavLink>
            <NavLink
                to="/air-stripper-readings"
                className={({ isActive }) => (isActive ? "active-navlink" : "navlink")}
            >
                Air Stripper Readings
            </NavLink>
        </div>
    )
}