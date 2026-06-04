import './index.css';
import Header from "./components/Header"; 
import Toolbar from "./components/Toolbar"
import DataChart from "./components/DataChart";
import StatsSidebar from './components/StatsSidebar';

function App() {
  return (
    <div className="min-h-screen bg-black text-white">
      <Header />
      <main className="flex flex-row h-[60%] border-b border-white/10">
        <div className="basis-3/4 m-4 p-8 flex flex-col items-center">
          <Toolbar />
          <DataChart />
        </div>
        <aside className="basis-1/4 bg-[#141418] p-8">
          <StatsSidebar />
        </aside>
      </main>
      <div>
        Stats
      </div>
      <footer className="bg-[#141418] w-full p-4 border-t border-white/10">
        All Rights Reserved
      </footer>
    </div>  
  )
}

export default App
