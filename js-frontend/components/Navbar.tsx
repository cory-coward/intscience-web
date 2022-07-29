import React from "react";
import { NavLink } from "react-router-dom";

export default function Navbar() {
    return (
        <div className="mb-6 px-10 bg-gray-800 space-x-6">
            <NavLink
                to="/"
                className={({ isActive }) => (isActive ? "active-navlink" : "navlink")}
            >
                Home
            </NavLink>
            <NavLink
                to="/about"
                className={({ isActive }) => (isActive ? "active-navlink" : "navlink")}
            >
                About
            </NavLink>
        </div>
    )
}