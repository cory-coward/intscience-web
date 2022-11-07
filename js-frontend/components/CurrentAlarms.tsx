import React, {useEffect, useState} from "react";
import axios, { AxiosError } from "axios";
import { format } from "date-fns";
import LoadingComponent from "./LoadingComponent";

interface ICurrentAlarmEntry {
    alarm_tag: string;
    alarm_description: string;
    dial: boolean;
    alarm_time: string;
    ack_time?: string;
    clear_time?: string;
}

export default function CurrentAlarms() {
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [alarmEntries, setAlarmEntries] = useState<ICurrentAlarmEntry[]>([]);

    const loadData = () => {
        axios.get<ICurrentAlarmEntry[]>("/api/v1/plc-alarms/current-alarms")
            .then(res => {
                const entries: ICurrentAlarmEntry[] = [];

                res.data.forEach(entry => {
                    const entryToAdd: ICurrentAlarmEntry = {
                        alarm_tag: entry.alarm_tag,
                        alarm_description: entry.alarm_description,
                        dial: entry.dial,
                        alarm_time: format(new Date(entry.alarm_time.toString()), "MMM d, yyyy hh:mm:ss a"),
                        ack_time: entry.ack_time ? (new Date(entry.ack_time.toString()), "MMM d, yyyy hh:mm:ss a") : "",
                        clear_time: entry.clear_time ? format(new Date(entry.clear_time.toString()), "MMM d, yyyy hh:mm:ss a") : "",
                    }

                    entries.push(entryToAdd);
                });

                setAlarmEntries(entries);
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

    if (isLoading) return <LoadingComponent />;

    return (
        <>
            <div className="max-w-5xl mx-auto my-12">
                <div className="flex justify-between items-center">
                    <h2 className="font-bold text-2xl text-gray-700">Current Alarms</h2>
                </div>
                {alarmEntries.length === 0 ? (
                    <p className="text-sm text-gray-500">There are no currently active alarms.</p>
                ) : (
                    <div className="mt-8 flex flex-col">
                        <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
                            <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
                                <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
                                    <table className="min-w-full divide-y divide-gray-300">
                                        <thead className="bg-gray-50">
                                            <tr>
                                                <th scope="col" className="py-3 pl-4 pr-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500 sm:pl-6">
                                                    Alarm Tag
                                                </th>
                                                <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                    Alarm Description
                                                </th>
                                                <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                    Receives Emails?
                                                </th>
                                                <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                    Alarm Time
                                                </th>
                                                <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                    Acknowledged Time
                                                </th>
                                                <th scope="col" className="px-3 py-3 text-left text-xs font-medium uppercase tracking-wide text-gray-500">
                                                    Clear Time
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody className="bg-white">
                                        {alarmEntries.map((entry, entryId) => (
                                            <tr
                                                key={entry.alarm_tag}
                                                className={entryId % 2 === 0 ? undefined : "bg-gray-50"}
                                            >
                                                <td className="whitespace-nowrap py-2 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                                                    {entry.alarm_tag}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                    {entry.alarm_description}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                    {entry.dial ? "Yes" : "No"}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                    {entry.alarm_time}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                    {entry.ack_time}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-2 text-sm text-gray-500">
                                                    {entry.clear_time}
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
        </>
    )
}