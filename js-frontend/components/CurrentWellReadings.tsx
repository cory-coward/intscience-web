import React, { useEffect, useState } from "react";
import axios from "axios";
import LoadingComponent from "./LoadingComponent";

interface IWellLogEntry {
    id: number;
    well_name: string;
    gal_per_minute: number;
    total_gal: number;
    is_running: boolean;
    timestamp: Date;
}

export default function Home() {
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [wellLogEntries, setWellLogEntries] = useState<IWellLogEntry[]>([]);

    useEffect(() => {
        axios.get<IWellLogEntry[]>("/api/v1/well-logs/current-well-logs")
            .then(res => {
                setWellLogEntries(res.data);
                setIsLoading(false);
            })
            .catch(error => {
                console.error(error);
                setIsLoading(false);
            })
    }, []);

    if (isLoading) return <LoadingComponent />;

    return (
        <div className="max-w-5xl mx-auto my-12">
            <h2 className="mb-4 font-bold text-2xl text-gray-700">Current Well Readings</h2>
            {wellLogEntries.length === 0 ? (
                <p className="text-sm text-gray-500">No well readings have been recorded yet.</p>
            ) : (
                <div className="mt-8 flex flex-col">
                    <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
                        <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
                            <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
                                <table className="min-w-full divide-y divide-gray-300">
                                    <thead className="bg-gray-50">
                                        <tr>
                                            <th scope="col" className="py-3 pl-4 pr-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500 sm:pl-6">
                                                Well Name
                                            </th>
                                            <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                Gallons Per Minute
                                            </th>
                                            <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                Total Gallons
                                            </th>
                                            <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                Status
                                            </th>
                                            <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                Time Read
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody className="bg-white">
                                    {wellLogEntries.map((entry, entryId) => (
                                        <tr
                                            key={entry.id}
                                            className={entryId % 2 === 0 ? undefined : "bg-gray-50"}
                                        >
                                            <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                                                {entry.well_name}
                                            </td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                                {entry.gal_per_minute}
                                            </td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                                {entry.total_gal}
                                            </td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                                {entry.is_running ? "Running" : "Stopped"}
                                            </td>
                                            <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                                {entry.timestamp.toString()}
                                            </td>
                                        </tr>
                                    ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}