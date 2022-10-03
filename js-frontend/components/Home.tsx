import React, { useEffect, useState } from "react";
import axios from "axios";
import {Link} from "react-router-dom";

interface IWellLogEntry {
    id: number;
    well_name: string;
    gal_per_minute: number;
    total_gal: number;
    timestamp: Date;
}

export default function Home() {
    const [wellLogEntries, setWellLogEntries] = useState<IWellLogEntry[]>([]);

    useEffect(() => {
        axios.get<IWellLogEntry[]>("/api/v1/well-logs/current-well-logs")
            .then(res => {
                setWellLogEntries(res.data);
            })
            .catch(error => {
                console.error(error);
            })
    }, []);

    return (
        <div className="px-10">
            <h2>This is the <span className="font-extrabold text-sky-500">home</span> page, EDITED.</h2>
            {wellLogEntries.map(entry => (
                <p key={entry.id}>
                    {entry.well_name}
                </p>
            ))}
        </div>
    )
}