import { Link, useLocation } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
    const location = useLocation();
    
    return (
        <nav className="navbar glass-panel" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '15px 30px' }}>
            <div className="navbar-brand" style={{ display: 'flex', alignItems: 'center' }}>
                <span className="logo-icon" style={{ fontSize: '24px', marginRight: '10px' }}>💰</span>
                <span className="logo-text text-gradient" style={{ fontSize: '24px', fontWeight: 'bold' }}>Finora</span>
            </div>
            
            <div className="navbar-links" style={{ display: "flex", gap: "2rem", flex: 1, marginLeft: "3rem" }}>
                <Link to="/" style={{ color: location.pathname === "/" ? "var(--primary-color)" : "white", textDecoration: "none", fontWeight: location.pathname === "/" ? "bold" : "normal" }}>Dashboard</Link>
                <Link to="/transactions" style={{ color: location.pathname === "/transactions" ? "var(--primary-color)" : "white", textDecoration: "none", fontWeight: location.pathname === "/transactions" ? "bold" : "normal" }}>Transactions</Link>
                <Link to="/categories" style={{ color: location.pathname === "/categories" ? "var(--primary-color)" : "white", textDecoration: "none", fontWeight: location.pathname === "/categories" ? "bold" : "normal" }}>Categories</Link>
                <Link to="/loans" style={{ color: location.pathname === "/loans" ? "var(--primary-color)" : "white", textDecoration: "none", fontWeight: location.pathname === "/loans" ? "bold" : "normal" }}>Loans & EMIs</Link>
            </div>

            <div className="navbar-actions">
                <div className="avatar" style={{ background: 'var(--primary-color)', width: '40px', height: '40px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>
                    U
                </div>
            </div>
        </nav>
    );
}

export default Navbar;