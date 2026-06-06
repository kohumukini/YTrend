import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts"; 
import { type ChartDataPoint } from "../types/index"

type DataChart = {
    data: ChartDataPoint[]; 
    errorMessage?: string; 
}

const DataChart = ({ data, errorMessage }: DataChart) => {
    if (errorMessage) return <h1>{errorMessage}</h1>
    

    return (
        <ResponsiveContainer width='100%' aspect={1.618} >
            <LineChart data={data} margin={{top: 20, right: 20, bottom: 20, left: 20}}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                    dataKey="date"
                    scale="time"
                    type="number"
                    domain={['auto', 'auto']}
                    tickFormatter={(ms) => new Date(ms).toLocaleDateString()}
                />
                <YAxis
                    tickFormatter={(value) => `$${value}`}
                    width={70}
                    domain={['auto', 'auto']}
                />

                <Tooltip
                    labelFormatter={(ms) => new Date(ms).toLocaleDateString()}
                    formatter={(value) => [`$${Number(value).toFixed(2)}`]}
                />
                <Legend />

                {/* Main price */}
                <Line type="monotone" dataKey="close" stroke="#ffffff" dot={false} name="Close" />

                {/* SMA's*/}
                <Line type="monotone" dataKey="sma_20" stroke="#4ade80" dot={false} name="SMA 20" />
                <Line type="monotone" dataKey="sma_50" stroke="#facc15" dot={false} name="SMA 50" />
                <Line type="monotone" dataKey="sma_100" stroke="#fb923c" dot={false} name="SMA 100" />

                {/* Bollinger Bands */}
                <Line type="monotone" dataKey="bb_upper_30" stroke="#60a5fa" dot={false} strokeDasharray="4 4" name="BB Upper" />
                <Line type="monotone" dataKey="bb_mid_30" stroke="#818cf8" dot={false} strokeDasharray="4 4" name="BB Mid" />
                <Line type="monotone" dataKey="bb_lower_30" stroke="#60a5fa" dot={false} strokeDasharray="4 4" name="BB Lower" />
            </LineChart>
        </ResponsiveContainer>
    );
};


export default DataChart;