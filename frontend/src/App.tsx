import './index.css';
import Header from "./components/Header"; 
import Toolbar from "./components/Toolbar"

function App() {
  return (
    <div className="h-screen bg-black text-white">
      <Header />
      <main className="flex flex-row h-[60%] border-b border-white/10">
        <div className="basis-3/4 m-4 p-8">
          <Toolbar />
          <div className="bg-[#141418] w-full h-[80%] my-4">
            Chart
          </div>
        </div>
        <aside className="basis-1/4 bg-[#141418]">
          <div>
            Sidebar
          </div>
        </aside>
      </main>
      <div>
        Stats
      </div>
      <footer className="bg-[#141418] bottom-0 fixed w-full p-4 border-t border-white/10">
        All Rights Reserved
      </footer>
    </div>  
  )
}

export default App
