const Header = ({toggleTheme, isDarkMode}) => {
    return(
    <div>
        {/* Top Navigation Bar */}
        <header className="top-nav">
            <div className="nav-links">
                <a href="/#home">Home</a>
                <a href="/#features">Features</a>
                <a href="/#data-selection">Data Selection</a>
                <a href="/#graphs">Graphs</a>
                <a href="/login">Login</a>
            </div>
            <button onClick={toggleTheme} className="theme-toggle-btn">
            {isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            </button>
        </header>
    </div>
    )
}

export default Header