type ItemCardProps = {
    label: string; 
    value: string; 
    indicator?: string;
}

const ItemCard = ({ label, value, indicator }: ItemCardProps) => {
    return (
        <div className="w-full bg-[#212124] p-6 border border-white/5 rounded-3xl">
            <p className="text-[#818184]">{label}</p>
            <h4 className="text-2xl font-bold">{value}</h4>
            {indicator}
        </div>
    )
}

const StatsSidebar = () => {
    return (
        <div className="h-full flex flex-col gap-5">
            <h3 className="text-[#818184] font-bold">Live Data</h3>
            <ItemCard label="Current Price" value="$99.99" indicator="^ 2.4% today"/>
            <ItemCard label="Volume" value="20M" indicator="Down -5% vs avg"/>
            <ItemCard label="Market Cap" value="$1.4T"/>
            <ItemCard label="Yearly Range" value="$87-$104" />
        </div>
    )
}

export default StatsSidebar;