import React, { useEffect, useRef, useState } from "react";
import axios, { AxiosError } from "axios";
import { format } from "date-fns";
import { ArrowPathIcon, XMarkIcon } from "@heroicons/react/24/outline";
import { ExcelExport, ExcelExportColumn } from "@progress/kendo-react-excel-export";
import { toast } from "react-toastify";
import LoadingComponent from "./LoadingComponent";
import RunningStatusIndicator from "./RunningStatusIndicator";
import getCookie from "../helpers/getCookie";

interface IWellLogEntry {
    id: number;
    well_name: string;
    gal_per_minute: number;
    total_gal: number;
    pump_mode: string;
    is_running: boolean;
    timestamp: string;
}

enum PumpMode {
    Auto = "Auto",
    Manual = "Manual",
}

export default function Home() {
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [wellLogEntries, setWellLogEntries] = useState<IWellLogEntry[]>([]);
    const exportRef = useRef<ExcelExport | null>(null);

    const buttonBase: string = "px-3 py-1 inline-flex items-center gap-1.5 bg-transparent border rounded transition-colors duration-150"
    const buttonStart: string = "text-emerald-600 border-emerald-600 hover:bg-emerald-600 hover:text-white";
    const buttonStop: string = "text-red-600 border-red-600 hover:bg-red-600 hover:text-white";
    const disabledButton: string = "text-gray-500 border-gray-300";

    const loadData = () => {
        axios.get<IWellLogEntry[]>("/api/v1/plc-logs/current-well-logs")
            .then(res => {
                const entriesFromServer: IWellLogEntry[] = [];

                res.data.forEach(entry => {
                    const entryToAdd: IWellLogEntry = {
                        id: entry.id,
                        well_name: entry.well_name,
                        gal_per_minute: entry.gal_per_minute,
                        total_gal: entry.total_gal,
                        pump_mode: entry.pump_mode,
                        is_running: entry.is_running,
                        timestamp: format(new Date(entry.timestamp.toString()), "MMM d, yyyy hh:mm:ss a"),
                    }

                    entriesFromServer.push(entryToAdd);
                });

                setWellLogEntries(entriesFromServer);
                setIsLoading(false);
            })
            .catch(error => {
                console.error(error);
                setIsLoading(false);
            });
    }

    useEffect(() => {
        loadData();

        (function loop() {
            setTimeout(() => {
                loadData();
                loop();
            }, 10000);
        })();
    }, []);

    const handleMachineOperation = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>, wellName: string, newPumpMode: PumpMode) => {
        setIsLoading(true);
        e.preventDefault();
        const target = e.currentTarget as HTMLInputElement;
        target.disabled = true;
        target.classList.remove(...buttonStart.split(" "));
        target.classList.remove(...buttonStop.split(" "));
        target.classList.add(...disabledButton.split(" "));
        target.innerHTML = "Please wait...";

        axios.post("/api/v1/well-logs/set-pump-mode/", {
            well_name: wellName,
            new_mode: newPumpMode,
        }, {
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
            .then(res => {
                loadData();
                target.disabled = false;
                target.classList.remove(...disabledButton.split(" "));

                switch (newPumpMode) {
                    case PumpMode.Auto:
                        target.classList.add(...buttonStop.split(" "));
                        target.innerHTML = `${<XMarkIcon className="w-5 h-5" />}Set to Manual`;
                        break;
                    case PumpMode.Manual:
                        target.classList.add(...buttonStart.split(" "));
                        target.innerHTML = `${<ArrowPathIcon className="w-5 h-5" />}Set to Auto`;
                        break;
                    default:
                        break;
                }
                setIsLoading(false);
            })
            .catch((error: AxiosError) => {
                if (error.response) {
                    if (error.response.status === 403) {
                        toast.error("You do not have sufficient permission to perform this action.");
                    }
                }
                setIsLoading(false);
            });
    };

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
                    <h2 className="font-bold text-2xl text-gray-700">Current Well Readings</h2>
                    <button className="button" onClick={excelExport}>
                        Export to Excel
                    </button>
                </div>
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
                                                    Time Read
                                                </th>
                                                <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                    Status
                                                </th>
                                                <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                    Pump Mode
                                                </th>
                                                <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                    Actions
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody className="bg-white">
                                        {wellLogEntries.map((entry, entryId) => (
                                            <tr
                                                key={entry.well_name}
                                                className={entryId % 2 === 0 ? undefined : "bg-gray-50"}
                                            >
                                                <td className="whitespace-nowrap py-2 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                                                    {entry.well_name}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                    {entry.gal_per_minute.toFixed(1)}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                    {entry.total_gal.toFixed(1)}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                    {format(new Date(entry.timestamp.toString()), "MMM d, yyyy hh:mm:ss a")}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                    <RunningStatusIndicator isRunning={entry.is_running} />
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                    {entry.pump_mode}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-1.5 text-sm text-gray-500">
                                                    {entry.pump_mode === PumpMode.Auto ? (
                                                        <button
                                                            onClick={(e) => handleMachineOperation(e, entry.well_name, PumpMode.Manual)}
                                                            className={`${buttonBase} ${buttonStop}`}
                                                        >
                                                            <XMarkIcon className="w-5 h-5" />Set to Manual
                                                        </button>
                                                    ) : (
                                                        <button
                                                            onClick={(e) => handleMachineOperation(e, entry.well_name, PumpMode.Auto)}
                                                            className={`${buttonBase} ${buttonStart}`}
                                                        >
                                                            <ArrowPathIcon className="w-5 h-5" />Set to Auto
                                                        </button>
                                                    )}
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
                data={wellLogEntries}
                fileName="WellReadings.xlsx"
                ref={exportRef}
            >
                <ExcelExportColumn field="well_name" title="Well Name" />
                <ExcelExportColumn field="gal_per_minute" title="Gallons per Minute" />
                <ExcelExportColumn field="total_gal" title="Total Gallons" />
                <ExcelExportColumn field="timestamp" title="Timestamp" />
                <ExcelExportColumn field="is_running" title="Is Running?" />
                <ExcelExportColumn field="pump_mode" title="Pump Mode" />
            </ExcelExport>
        </>
    )
}