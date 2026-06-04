import githubLogo from "../assets/github-logo.png";
import yahooLogo from "../assets/yahoo.png";

const Header = () => {
    return (
        <header>
            <nav className="flex flex-row justify-between gap-4 py-4 px-8 bg-[#141418] border-b border-white/10 items-center">
                <h1 className="text-[#FF6B2B] font-bold text-2xl">Dev</h1>
                <ul className="flex flex-row justify-evenly gap-16 list-none text-gray-400">
                    <li><a href="https://github.com/kohumukini/YTrend" target="_blank" ><img className="size-8 grayscale-100 brightness-600" src={githubLogo} /></a></li>
                    <li><a href="https://pypi.org/project/yfinance/" target="_blank" ><img className="size-8" src={yahooLogo} /></a></li>
                </ul>
            </nav>
        </header>
    )
}

export default Header;