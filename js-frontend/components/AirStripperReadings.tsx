import React, {useEffect, useRef, useState} from "react";
import axios, { AxiosError } from "axios";
import {format} from "date-fns";
import {ExcelExport, ExcelExportColumn} from "@progress/kendo-react-excel-export";
import LoadingComponent from "./LoadingComponent";

interface IAirStripperLogEntry {
    // id: number;
    air_stripper_name: string;
    pump_runtime: number;
    blower_runtime: number;
    timestamp: string;
}

export default function AirStripperReadings() {
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [airStripperLogEntries, setAirStripperLogEntries] = useState<IAirStripperLogEntry[]>([]);
    const exportRef = useRef<ExcelExport | null>(null);

    const loadData = () => {
        axios.get<IAirStripperLogEntry[]>("/api/v1/plc-logs/current-air-stripper-logs")
            .then(res => {
                const entries: IAirStripperLogEntry[] = [];

                res.data.forEach(entry => {
                    const entryToAdd: IAirStripperLogEntry = {
                        // id: entry.id,
                        air_stripper_name: entry.air_stripper_name,
                        pump_runtime: entry.pump_runtime,
                        blower_runtime: entry.blower_runtime,
                        timestamp: format(new Date(entry.timestamp.toString()), "MMM d, yyyy hh:mm:ss a"),
                    }

                    entries.push(entryToAdd);
                })

                setAirStripperLogEntries(entries);
                setIsLoading(false);
            })
            .catch((error: AxiosError) => {
                console.error(error);
                setIsLoading(false);
            });
    }

    useEffect(() => {
        loadData();
    }, []);

    const excelExport = () => {
        if (exportRef.current !== null) {
            exportRef.current.save();
        }
    }

    if (isLoading) return <LoadingComponent />;

    return (
        <>
            <div className="max-w-5xl mx-auto my-12">
                <div className="flex justify-between items-center">
                    <h2 className="font-bold text-2xl text-gray-700">Current Air Stripper Readings</h2>
                    <button className="button" onClick={excelExport}>
                        Export to Excel
                    </button>
                </div>
                {airStripperLogEntries.length === 0 ? (
                    <p className="text-sm text-gray-500">No air stripper readings have been recorded yet.</p>
                ) : (
                    <div className="mt-8 flex flex-col">
                        <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
                            <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
                                <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
                                    <table className="min-w-full divide-y divide-gray-300">
                                        <thead className="bg-gray-50">
                                            <tr>
                                                <th scope="col" className="py-3 pl-4 pr-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500 sm:pl-6">
                                                    Air Stripper Name
                                                </th>
                                                <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                    Pump Runtime
                                                </th>
                                                <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                    Blower Runtime
                                                </th>
                                                <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                    Time Read
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody className="bg-white">
                                        {airStripperLogEntries.map((entry, entryId) => (
                                            <tr
                                                key={entry.air_stripper_name}
                                                className={entryId % 2 === 0 ? undefined : "bg-gray-50"}
                                            >
                                                <td className="whitespace-nowrap py-2 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                                                    {entry.air_stripper_name}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                    {entry.pump_runtime.toFixed(1)}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                    {entry.blower_runtime.toFixed(1)}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                    {format(new Date(entry.timestamp.toString()), "MMM d, yyyy hh:mm:ss a")}
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

            <ExcelExport
                data={airStripperLogEntries}
                fileName="AirStripperReadings.xlsx"
                ref={exportRef}
            >
                <ExcelExportColumn field="air_stripper_name" title="Air Stripper Name" />
                <ExcelExportColumn field="pump_runtime" title="Pump Runtime" />
                <ExcelExportColumn field="blower_runtime" title="Blower Runtime" />
                <ExcelExportColumn field="timestamp" title="Timestamp" />
            </ExcelExport>
        </>
    )
}
