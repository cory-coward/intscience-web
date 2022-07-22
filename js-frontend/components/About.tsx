import React from "react";
import {Link} from "react-router-dom";

export default function About() {
    return (
        <>
            <h2>This is the <span className="font-extrabold text-sky-500">about</span> page.</h2>
            <Link to="/">Home</Link>
        </>
    )
}