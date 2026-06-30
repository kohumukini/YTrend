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
    const { forecast, signal, confidence, direction, last_month_pct_change } = data; 

    return (
        <div className="flex flex-col w-full items-center border-t border-white/10">
            <h3 className="text-2xl font-bold text-[#818184]">Predictions</h3>
            <section className="flex flex-row w-[80%] justify-evenly p-4 items-center">
                <ItemCard label="Next Month's Forecasted % Change" value={`${Number(forecast).toFixed(2)}%`} isOrange={true}/>
                <ItemCard label="Price Direction" value={direction} />
                <ItemCard label="Confidence % in Signal" value={`${Number(confidence).toFixed(2)}%`} />
                <ItemCard label="Signal" value={signal ? signal : "N/A"} isOrange={true}/>
                <ItemCard label="Last Month's Price % Change" value={Number(last_month_pct_change).toFixed(2)} />
            </section>
        </div>
    )
}

export default StatsAndPredictions; 