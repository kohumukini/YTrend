import { type RawSilverItem, type RawGoldItem, type RawWatchListItem } from "../types/index";
import { type ChartDataPoint, type SidebarStats, type PredictionData } from "../types/index"; 

const BASE_URL = 'http://localhost:8000'; 

// Transformation functions

export const SilverToChart = (raw: RawSilverItem[]): ChartDataPoint[] => {
    return [...raw].reverse().map(item => ({
        date: Date.parse(item.timestamp), 
        close: item.close_price, 
        rsi: item.rsi_14, 
        sma_20: item.sma_20, 
        sma_50: item.sma_50, 
        sma_100: item.sma_100, 
        bb_lower_30: item.bollinger_band_lower_30, 
        bb_mid_30: item.bollinger_band_mid_30, 
        bb_upper_30: item.bollinger_band_upper_30
    })); 
};

export const SilverToSidebar = (raw: RawSilverItem[]): SidebarStats => {
    const lastItem = raw[0]; 
    const secondToLastItem = raw[1];
    const pastYear = raw.slice(0, 252); 

    return {
        currentPrice: lastItem.close_price, 
        volume: lastItem.volume, 
        yearlyHigh: pastYear.reduce((max, item) => item.high > max ? item.high : max, raw[0].high), 
        yearlyLow: pastYear.reduce((min, item) => item.low < min ? item.low : min, raw[0].low), 
        volatility: lastItem.volatility_30 ?? 0,
        yesterdayPrice: secondToLastItem.close_price, 
        yesterdayVolume: secondToLastItem.volume, 
    };
};

export const GoldToPrediction = (raw: RawGoldItem[]): PredictionData => {
    const lastItem = raw[0]; 

    return {
        forecast: lastItem.lstm_prediction ?? 0, 
        signal: lastItem.buy_signal ?? 'N/A', 
        confidence: lastItem.confidence_score
    };
};

// Fetch Functions
export async function fetchSilverData(ticker: string): Promise<RawSilverItem[]> {
    const response = await fetch(`${BASE_URL}/silver/${ticker}/data`, {
        method: 'GET', 
        headers: {
            'Content-type': 'application/json', 
        },
    });

    if (!response.ok) {
        throw new Error(`Error fetching data for silver ticker ${ticker}: ${response.statusText}`)
    }

    return response.json(); 
}

// export async function fetchGoldData(ticker: string): Promise<RawGoldItem[]> {
//     const response = await fetch(`${BASE_URL}/${ticker}`, {
//         method: 'GET', 
//         headers: {
//             'Content-type': 'application/json', 
//         },
//     })
    
//     if (!response.ok) {
//         throw new Error(`Error fetching data for gold ticker ${ticker}: ${response.statusText}`)
//     }

//     return response.json(); 
// }

export async function fetchWatchListData(): Promise<RawWatchListItem[]> {
    const response = await fetch(`${BASE_URL}/watchlist/data`, {
        method: 'GET', 
        headers: {
            'Content-type': 'application/json', 
        },
    })

    if (!response.ok) {
        throw new Error(`Error fetching watchlist data: ${response.statusText}`);
    }

    return response.json()
}