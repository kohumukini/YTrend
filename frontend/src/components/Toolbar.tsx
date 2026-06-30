import { useState, useEffect, useCallback } from 'react';
import { fetchWatchListData } from '../services/api';
import { type RawWatchListItem } from '../types/index';

type ToolbarProps = {
    onClick: () => void;
    buttonText: string;
    activeTicker: string;
    onTickerChange: (ticker: string) => void;
}

const Toolbar = ({ onClick, buttonText, activeTicker, onTickerChange }: ToolbarProps) => {
    const [watchlist, setWatchlist] = useState<RawWatchListItem[]>([]);
    const [showDropdown, setShowDropdown] = useState(false);
    const [showAddInput, setShowAddInput] = useState(false);
    const [newTicker, setNewTicker] = useState('');

    const loadWatchlist = useCallback(async () => {
        try {
            const data = await fetchWatchListData();
            setWatchlist(data);
        } catch (err) {
            console.error("Failed to load watchlist:", err);
        }
    }, []);

    useEffect(() => {
        let isMounted = true;

        const load = async () => {
            try {
                const data = await fetchWatchListData();
                if (isMounted) {
                    setWatchlist(data);
                }
            } catch (err) {
                if (isMounted) {
                    console.error("Failed to load watchlist:", err);
                }
            }
        };

        load();

        return () => {
            isMounted = false;
        };
    }, []);

    const handleAddTicker = async () => {
        if (!newTicker.trim()) return;
        try {
            await fetch(`http://localhost:8000/watchlist/add/${newTicker.toUpperCase()}`, {
                method: 'POST',
            });
            setNewTicker('');
            setShowAddInput(false);
            loadWatchlist();

            // Trigger pipeline to backfill the new ticker
            await fetch(`http://localhost:8000/pipeline/run`, {
                method: 'POST',
            });
        } catch (err) {
            console.error("Failed to add ticker:", err);
        }
    };

    const handleRemoveTicker = async (ticker: string) => {
        try {
            await fetch(`http://localhost:8000/watchlist/remove/${ticker}`, {
                method: 'DELETE',
            });
            loadWatchlist();
        } catch (err) {
            console.error("Failed to remove ticker:", err);
        }
    };

    const otherTickersCount = watchlist.filter(t => t.ticker !== activeTicker).length;

    return (
        <div className="w-full flex flex-row justify-between items-center">
            <section className="flex flex-row justify-between gap-4 items-center relative">
                <div className="border-[0.5px] border-[#FF6B2B] p-2 rounded-xl bg-[#212124] cursor-pointer"
                    onClick={() => setShowDropdown(!showDropdown)}>
                    {activeTicker}
                    <button className="text-[#ff6b2bca] bg-[#ff6b2b3c] py-.5 px-2 mx-2 my-1 rounded-lg border border-[#ff6b2b] text-center">
                        +{otherTickersCount}
                    </button>
                </div>

                {showDropdown && (
                    <div className="absolute top-12 left-0 bg-[#212124] border border-white/10 rounded-xl p-2 z-10 min-w-45">
                        {watchlist.map((item) => (
                            <div key={item.ticker} className="flex flex-row justify-between items-center p-2 hover:bg-white/5 rounded-lg">
                                <span
                                    className="cursor-pointer"
                                    onClick={() => {
                                        onTickerChange(item.ticker);
                                        setShowDropdown(false);
                                    }}
                                >
                                    {item.ticker}
                                </span>
                                <button
                                    className="text-red-400 text-sm px-2"
                                    onClick={() => handleRemoveTicker(item.ticker)}
                                >
                                    ✕
                                </button>
                            </div>
                        ))}
                    </div>
                )}

                {showAddInput ? (
                    <div className="border-[0.5px] border-white/5 p-2 rounded-xl bg-[#212124] flex flex-row gap-2 items-center">
                        <input
                            className="bg-transparent outline-none text-white w-20"
                            value={newTicker}
                            onChange={(e) => setNewTicker(e.target.value)}
                            placeholder="TICKER"
                            autoFocus
                            onKeyDown={(e) => e.key === 'Enter' && handleAddTicker()}
                        />
                        <button onClick={handleAddTicker} className="text-[#FF6B2B]">✓</button>
                    </div>
                ) : (
                    <div
                        className="border-[0.5px] border-white/5 p-2 rounded-xl bg-[#212124] cursor-pointer"
                        onClick={() => setShowAddInput(true)}
                    >
                        + Add ticker
                    </div>
                )}
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