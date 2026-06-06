type Toolbar = {
    onClick: () => void; 
    buttonText: string; 
}

const Toolbar = ({ onClick, buttonText }: Toolbar) => {
    return (
        <div className="w-full flex flex-row justify-between items-center">
            <section className="flex flex-row justify-between gap-4 items-center ">
                <div className="border-[0.5px] border-[#FF6B2B] p-2 rounded-xl bg-[#212124]">
                    AAPL 
                    <button className="text-[#ff6b2bca] bg-[#ff6b2b3c] py-.5 px-2 mx-2 my-1 rounded-lg border border-[#ff6b2b] text-center">
                        +2
                    </button>
                </div>
                <div className="border-[0.5px] border-white/5 p-2 rounded-xl bg-[#212124]">+ Add ticker</div>
            </section>
            <section>
                <button 
                    className="border-2 border-white/5 font-semibold rounded-lg py-2 px-4 cursor-pointer bg-[#FF6B2B] text-white shadow-[0_0_15px_5px_rgba(255,107,43,0.4)]"
                    onClick={onClick}
                >
                    {buttonText}
                </button>
            </section>
        </div>
    )
}

export default Toolbar; 