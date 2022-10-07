import React, { useEffect, useState } from "react";
import axios from "axios";
import { format } from "date-fns";
import { ArrowPathIcon, XMarkIcon } from "@heroicons/react/24/outline";
import LoadingComponent from "./LoadingComponent";
import RunningStatusIndicator from "./RunningStatusIndicator";
import getCookie from "../helpers/getCookie";

interface IWellLogEntry {
    id: number;
    well_name: string;
    gal_per_minute: number;
    total_gal: number;
    is_running: boolean;
    timestamp: Date;
}

enum MachineOperation {
    Start = "START",
    Stop = "STOP",
}

export default function Home() {
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [wellLogEntries, setWellLogEntries] = useState<IWellLogEntry[]>([]);

    const buttonBase: string = "px-3 py-1 inline-flex items-center gap-1.5 bg-transparent border rounded transition-colors duration-150"
    const buttonStart: string = "text-emerald-600 border-emerald-600 hover:bg-emerald-600 hover:text-white";
    const buttonStop: string = "text-red-600 border-red-600 hover:bg-red-600 hover:text-white";
    const disabledButton: string = "text-gray-500 border-gray-300";

    const loadData = () => {
        axios.get<IWellLogEntry[]>("/api/v1/well-logs/current-well-logs")
            .then(res => {
                setWellLogEntries(res.data);
                console.log(res.data);
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

    const handleMachineOperation = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>, wellName: string, newMachineState: MachineOperation) => {
        setIsLoading(true);
        e.preventDefault();
        const target = e.currentTarget as HTMLInputElement;
        target.disabled = true;
        target.classList.remove(...buttonStart.split(" "));
        target.classList.remove(...buttonStop.split(" "));
        target.classList.add(...disabledButton.split(" "));
        target.innerHTML = "Please wait...";

        console.log(`${wellName}: ${newMachineState.toString()}`);

        axios.post("/api/v1/well-logs/set-well-state/", {
            well_name: "Hello",
            new_state: "World",
        }, {
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
            .then(res => {
                console.log(res.data);
                loadData();
                target.disabled = false;
                target.classList.remove(...disabledButton.split(" "));

                switch (newMachineState) {
                    case MachineOperation.Start:
                        target.classList.add(...buttonStop.split(" "));
                        target.innerHTML = `${<XMarkIcon className="w-5 h-5" />}Stop`;
                        break;
                    case MachineOperation.Stop:
                        target.classList.add(...buttonStart.split(" "));
                        target.innerHTML = `${<ArrowPathIcon className="w-5 h-5" />}Start`;
                        break;
                    default:
                        break;
                }
                setIsLoading(false);
            })
            .catch(error => {
                console.error(error);
                setIsLoading(false);
            });
    };

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
                                                Time Read
                                            </th>
                                            <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                Status
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
                                                {entry.gal_per_minute}
                                            </td>
                                            <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                {entry.total_gal}
                                            </td>
                                            <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                {format(new Date(entry.timestamp.toString()), "MMM d, yyyy hh:mm:ss a")}
                                            </td>
                                            <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                <RunningStatusIndicator isRunning={entry.is_running} />
                                            </td>
                                            <td className="whitespace-nowrap px-3 py-1.5 text-sm text-gray-500">
                                                {entry.is_running ? (
                                                    <button
                                                        onClick={(e) => handleMachineOperation(e, entry.well_name, MachineOperation.Stop)}
                                                        className={`${buttonBase} ${entry.is_running ? buttonStop : buttonStart}`}
                                                    >
                                                        <XMarkIcon className="w-5 h-5" />Stop
                                                    </button>
                                                ) : (
                                                    <button
                                                        onClick={(e) => handleMachineOperation(e, entry.well_name, MachineOperation.Start)}
                                                        className={`${buttonBase} ${entry.is_running ? buttonStop : buttonStart}`}
                                                    >
                                                        <ArrowPathIcon className="w-5 h-5" />Start
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
    )
}