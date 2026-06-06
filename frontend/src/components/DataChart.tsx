import { RechartsDevtools } from "@recharts/devtools";
import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts"; 
import { type ChartDataPoint } from "../types/index"

type DataChart = {
    data: ChartDataPoint[]; 
    errorMessage?: string; 
}

const DataChart = ({ data, errorMessage }: DataChart) => {
    if (errorMessage) return <h1>{errorMessage}</h1>

    return (
        <ResponsiveContainer width='100%' aspect={1.618} >
            <ScatterChart margin={{ top: 20, right: 0, bottom: 0, left: 0, }}>
                <CartesianGrid />
                <XAxis type="number" dataKey="x" name="stature" unit="cm" />
                <YAxis type="number" dataKey="y" name="weight" unit="kg" width="auto" />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                <Scatter activeShape={{ fill: 'red' }} name="A school" data={data} fill="#8884d8" />
                <RechartsDevtools />
            </ScatterChart>
        </ResponsiveContainer>
    );
};


export default DataChart;