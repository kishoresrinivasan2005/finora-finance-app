import { useEffect, useState } from "react";
import { getTransactionsSummary, createTransaction, getCategories } from "../api/services";
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
    ResponsiveContainer
} from "recharts";
import "./Dashboard.css";

const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
        return (
            <div className="custom-tooltip glass-panel" style={{borderRadius: "8px", border: "1px solid rgba(255,255,255,0.1)", padding: "10px"}}>
                <p className="label" style={{margin: 0, color: "white"}}>{label}</p>
                <p className="amount" style={{margin: 0, fontWeight: "bold", color: "var(--primary-color)"}}>₹ {payload[0].value.toLocaleString()}</p>
            </div>
        );
    }
    return null;
};

function Dashboard() {
    const [data, setData] = useState(null);
    const [chartData, setChartData] = useState([]);
    const [categories, setCategories] = useState([]);
    
    // Form state
    const [amount, setAmount] = useState("");
    const [type, setType] = useState("expense");
    const [categoryId, setCategoryId] = useState("");
    
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        fetchData();
        fetchCategories();
    }, []);

    const fetchCategories = async () => {
        try {
            const data = await getCategories();
            setCategories(data);
            if (data.length > 0) setCategoryId(data[0].id);
        } catch (err) {
            console.log("Error fetching categories", err);
        }
    }

    const fetchData = async () => {
        setIsLoading(true);
        try {
            const res = await getTransactionsSummary("current-month");
            setData(res);

            const chartRes = await getTransactionsSummary("monthly-expense-trend");
            setChartData(chartRes);
        } catch (err) {
            console.log(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleAddTransaction = async (e) => {
        e.preventDefault();
        if (!amount || amount <= 0 || !categoryId) return;

        try {
            await createTransaction({
                user_id: 1,
                amount: Number(amount),
                transaction_type: type,
                category_id: Number(categoryId),
                payment_mode: "cash"
            });

            fetchData();
            setAmount("");
        } catch (err) {
            console.log(err);
            alert("Error adding transaction");
        }
    };

    if (isLoading && !data) return (
        <div className="dashboard-container" style={{justifyContent: "center", alignItems: "center", minHeight: "60vh"}}>
            <div className="text-gradient" style={{fontSize: "24px", fontWeight: "600"}}>Loading Dashboard...</div>
        </div>
    );

    return (
        <div className="dashboard-container fade-in">
            <div className="dashboard-header">
                <h2 className="dashboard-title text-gradient">Dashboard</h2>
                <button className="glass-button" onClick={fetchData}>
                    <span style={{fontSize: "18px"}}>↻</span> Refresh
                </button>
            </div>

            <div className="summary-cards">
                <div className="summary-card glass-panel card-income">
                    <h3>
                        <span style={{color: "var(--success-color)", fontSize: "18px"}}>↓</span> Income
                    </h3>
                    <p style={{ color: "white" }}>₹ {data?.income?.toLocaleString() || 0}</p>
                </div>

                <div className="summary-card glass-panel card-expense">
                    <h3>
                        <span style={{color: "var(--danger-color)", fontSize: "18px"}}>↑</span> Expense
                    </h3>
                    <p style={{ color: "white" }}>₹ {data?.expense?.toLocaleString() || 0}</p>
                </div>

                <div className="summary-card glass-panel card-balance">
                    <h3>
                        <span style={{color: "var(--primary-color)", fontSize: "18px"}}>💳</span> Balance
                    </h3>
                    <p style={{ color: "white" }}>₹ {data?.balance?.toLocaleString() || 0}</p>
                </div>
            </div>

            <div className="dashboard-main">
                <div className="chart-section glass-panel">
                    <h3>Monthly Expense Trend</h3>
                    <div style={{ width: "100%", height: 350, marginTop: "10px" }}>
                        <ResponsiveContainer>
                            <LineChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                                <XAxis dataKey="month" axisLine={false} tickLine={false} dy={10} />
                                <YAxis axisLine={false} tickLine={false} dx={-10} tickFormatter={(value) => `₹${value}`} />
                                <Tooltip content={<CustomTooltip />} cursor={{ stroke: 'rgba(255,255,255,0.1)', strokeWidth: 2 }} />
                                <Line 
                                    type="monotone" dataKey="total_expense" stroke="var(--danger-color)" strokeWidth={3}
                                    dot={{ r: 4, fill: "var(--bg-color)", strokeWidth: 2, stroke: "var(--danger-color)" }}
                                    activeDot={{ r: 6, fill: "var(--danger-color)", strokeWidth: 0 }}
                                    animationDuration={1500}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="transaction-section glass-panel">
                    <h3>Add Transaction</h3>
                    
                    <form onSubmit={handleAddTransaction} style={{display: 'flex', flexDirection: 'column', gap: '20px', marginTop: '10px'}}>
                        <div className="form-group">
                            <label>Amount (₹)</label>
                            <input
                                type="number" className="glass-input" placeholder="e.g. 500" value={amount}
                                onChange={(e) => setAmount(e.target.value)} required min="1"
                            />
                        </div>

                        <div className="form-group">
                            <label>Type</label>
                            <div style={{ position: 'relative' }}>
                                <select 
                                    className="glass-input" value={type} onChange={(e) => setType(e.target.value)}
                                    style={{ appearance: 'none', color: 'white' }}
                                >
                                    <option value="income" style={{color: 'black'}}>Income</option>
                                    <option value="expense" style={{color: 'black'}}>Expense</option>
                                </select>
                                <div style={{ position: 'absolute', right: '16px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none', color: 'var(--text-secondary)', fontSize: '12px' }}>▼</div>
                            </div>
                        </div>

                        <div className="form-group">
                            <label>Category</label>
                            <div style={{ position: 'relative' }}>
                                <select 
                                    className="glass-input" value={categoryId} onChange={(e) => setCategoryId(e.target.value)}
                                    style={{ appearance: 'none', color: 'white' }} required
                                >
                                    {categories.map(cat => (
                                        <option key={cat.id} value={cat.id} style={{color: 'black'}}>{cat.name}</option>
                                    ))}
                                    {categories.length === 0 && <option value="" disabled style={{color: 'black'}}>No categories found</option>}
                                </select>
                                <div style={{ position: 'absolute', right: '16px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none', color: 'var(--text-secondary)', fontSize: '12px' }}>▼</div>
                            </div>
                        </div>

                        <button type="submit" className="glass-button" style={{ marginTop: '16px', width: '100%', padding: '14px' }}>
                            <span style={{fontSize: "20px", lineHeight: 1}}>+</span> Add Transaction
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;