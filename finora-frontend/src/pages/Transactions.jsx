import { useEffect, useState } from "react";
import { getTransactions } from "../api/services";

function Transactions() {
    const [transactions, setTransactions] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [typeFilter, setTypeFilter] = useState("");

    const fetchTransactions = async () => {
        setIsLoading(true);
        try {
            const params = typeFilter ? { transaction_type: typeFilter } : {};
            const data = await getTransactions(params);
            setTransactions(data);
        } catch (err) {
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchTransactions();
    }, [typeFilter]);

    return (
        <div className="dashboard-container fade-in">
            <div className="dashboard-header">
                <h2 className="dashboard-title text-gradient">Transactions</h2>
                <div style={{ display: 'flex', gap: '15px' }}>
                    <select 
                        className="glass-input" 
                        value={typeFilter} 
                        onChange={(e) => setTypeFilter(e.target.value)}
                        style={{ padding: '8px 15px', color: 'white', background: 'rgba(255,255,255,0.05)' }}
                    >
                        <option value="" style={{color: 'black'}}>All Types</option>
                        <option value="income" style={{color: 'black'}}>Income</option>
                        <option value="expense" style={{color: 'black'}}>Expense</option>
                    </select>
                    <button className="glass-button" onClick={fetchTransactions}>
                        <span style={{fontSize: "18px"}}>↻</span> Refresh
                    </button>
                </div>
            </div>

            <div className="dashboard-main" style={{ display: "block" }}>
                <div className="chart-section glass-panel" style={{ minHeight: "60vh" }}>
                    {isLoading ? <p style={{ color: "var(--text-secondary)" }}>Loading transactions...</p> : (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                            {transactions.length === 0 && <p style={{ color: "var(--text-secondary)" }}>No transactions found.</p>}
                            {transactions.map(txn => (
                                <div key={txn.id} className="glass-panel" style={{ display: 'flex', justifyContent: 'space-between', padding: '15px 20px', alignItems: 'center', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)' }}>
                                    <div>
                                        <div style={{ fontWeight: 'bold', fontSize: '18px', color: 'white' }}>₹ {txn.amount?.toLocaleString()}</div>
                                        <div style={{ color: 'var(--text-secondary)', fontSize: '13px', marginTop: '6px' }}>
                                            {new Date(txn.created_at).toLocaleString()} • {txn.payment_mode || 'N/A'}
                                        </div>
                                    </div>
                                    <div style={{ textTransform: 'capitalize', color: txn.transaction_type === 'income' ? 'var(--success-color)' : 'var(--danger-color)', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '10px', fontSize: '16px' }}>
                                        {txn.transaction_type === "income" ? "↓ " : "↑ "}
                                        {txn.transaction_type}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Transactions;
