import { useState } from 'react'; 
import './index.css';

// API requests
import { SilverToChart, SilverToSidebar, GoldToPrediction, fetchSilverData, fetchGoldData } from "./services/api"; 

// Type imports
import { type ChartDataPoint, type SidebarStats, type PredictionData } from "./types/index"; 

// Components
import Header from "./components/Header"; 
import Toolbar from "./components/Toolbar"
import DataChart from "./components/DataChart";
import StatsSidebar from './components/StatsSidebar';
import StatsAndPredictions from "./components/StatsAndPredictions";
import Footer from "./components/Footer";

type DashboardState = {
  ticker: string;
  chartData: ChartDataPoint[]; 
  sidebarStats: SidebarStats | null; 
  predictionData: PredictionData | null; 
}

const App = () => {
  const [dashboard, setDashboard] = useState<DashboardState>({
    ticker: "AAPL", 
    chartData: [],
    sidebarStats: null, 
    predictionData: null,  
  })

  const [isLoading, setIsLoading] = useState<boolean>(false); 
  const [error, setError] = useState<string | null>(null);
  // Consider using abort controller in the future
  const handleRun = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const silverRaw = await fetchSilverData(dashboard.ticker)
      const goldRaw = await fetchGoldData(dashboard.ticker)
      
      setDashboard((prevDash) => ({
        ...prevDash, 
        chartData: SilverToChart(silverRaw), 
        sidebarStats: SilverToSidebar(silverRaw), 
        predictionData: GoldToPrediction(goldRaw), 
      }))
    } catch (err) {
      setError("Failed to fetch data"); 
      console.error("Pipeline failed:", err); 
    } finally {
      setIsLoading(false)
    }
  }

  

  return (
    <div className="min-h-screen bg-black text-white">
      <Header />
      <main className="flex flex-row h-[60%] border-b border-white/10">
        <div className="basis-3/4 m-4 p-8 flex flex-col items-center">
          <Toolbar onClick={handleRun} buttonText={isLoading ? "Loading..." : "▷ Run"}/>
          <DataChart data={dashboard.chartData} errorMessage={error ? error : undefined}/>
        </div>
        <aside className="basis-1/4 bg-[#141418] p-8 border-l border-white/10">
          <StatsSidebar data={dashboard.sidebarStats} />
        </aside>
      </main>
      <StatsAndPredictions data={dashboard.predictionData} />
      <Footer />
    </div>  
  )
}

export default App
