import { type SidebarStats } from "../types/index";

type ItemCardProps = {
    label: string; 
    value: string; 
    indicator?: string;
    isPositive?: boolean;
}

const ItemCard = ({ label, value, indicator, isPositive }: ItemCardProps) => {
    return (
        <div className="w-full bg-[#212124] p-6 border border-white/5 rounded-3xl">
            <p className="text-[#818184]">{label}</p>
            <h4 className="text-2xl font-bold">{value}</h4>
            {indicator && (
                <p className={isPositive ? "text-green-400" : "text-red-400"}>{indicator}</p>
            )}
        </div>
    )
}

const StatsSidebar = ({ data }: { data: SidebarStats | null }) => {
    if (!data) return <p className="text-[#818184]">No Data Yet</p>;
    const { currentPrice, volume, volatility, yearlyHigh, yearlyLow } = data; 


    return (
        <div className="h-full flex flex-col gap-5">
            <h3 className="text-[#818184] font-bold">Live Data</h3>
            <ItemCard label="Current Price" value={`$${currentPrice}`} indicator="↑ 2.4% today" isPositive={true}/>
            <ItemCard label="Volume" value={`${volume}`} indicator="↓ -5% vs avg" isPositive={false}/>
            <ItemCard label="Volatility" value={`${volatility}`}/>
            <ItemCard label="Yearly Range" value={`${yearlyLow}-${yearlyHigh}`} />
        </div>
    );
}

export default StatsSidebar;