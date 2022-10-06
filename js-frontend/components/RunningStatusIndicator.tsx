import React from "react";

interface Props {
    isRunning: boolean
}

export default function RunningStatusIndicator({ isRunning }: Props) {
    return (
        <div>
            <span
                className={isRunning ? "text-emerald-600" : "text-amber-600"}
            >
                {isRunning ? "Running" : "Stopped"}
            </span>
        </div>
    )
}