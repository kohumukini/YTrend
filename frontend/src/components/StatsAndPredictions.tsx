import { type PredictionData } from "../types/index";

type ItemCardProps = {
    label: string;
    value: string;
    isOrange?: boolean; 
}

const ItemCard = ({label, value, isOrange}: ItemCardProps) => {

    return (
        <div className="bg-[#212124] py-4 px-6 rounded-3xl w-[30%]">
            <p className="text-l">{label}</p>
            <p className={`text-3xl ${isOrange ? "text-[#FF6B2B]": "text-white"}`}>{value}</p>
        </div>
    )
}

const StatsAndPredictions = ({ data }: { data: PredictionData | null }) => {
    if (!data) return null; 
    const { forecast, confidence, signal } = data; 

    return (
        <div className="flex flex-col w-full items-center border-t border-white/10">
            <h3 className="text-2xl font-bold text-[#818184]">Statistics</h3>
            <section className="flex flex-row w-[80%] justify-evenly p-4 items-center ">
                <ItemCard label="P/E Ratio" value="20" />
                <ItemCard label="Div Yield" value="1%" />
                <ItemCard label="EPS" value="$2.00" />
            </section>
            <h3 className="text-2xl font-bold text-[#818184]">Predictions</h3>
            <section className="flex flex-row w-[80%] justify-evenly p-4 items-center">
                <ItemCard label="Tomorrow's Forecast" value={`$${forecast}`} isOrange={true}/>
                <ItemCard label="Confidence %" value={`${confidence}%`} />
                <ItemCard label="Signal" value={signal ? signal : "N/A"} isOrange={true}/>
            </section>
        </div>
    )
}

export default StatsAndPredictions; 