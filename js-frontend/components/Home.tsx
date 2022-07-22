import React from "react";
import {Link} from "react-router-dom";

export default function Home() {
    return (
        <>
            <h2>This is the <span className="font-extrabold text-sky-500">home</span> page.</h2>
            <Link to="/about">About</Link>
        </>
    )
}