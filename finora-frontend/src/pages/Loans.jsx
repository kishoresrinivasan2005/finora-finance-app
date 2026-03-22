import { useEffect, useState } from "react";
import { getLoans, createLoan, getLoanEmis, payEmi } from "../api/services";

function Loans() {
    const [loans, setLoans] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    
    // Form state
    const [lenderName, setLenderName] = useState("");
    const [principal, setPrincipal] = useState("");
    const [interest, setInterest] = useState("");
    const [tenure, setTenure] = useState("");
    const [startDate, setStartDate] = useState("");
    
    // EMI View State
    const [selectedLoanId, setSelectedLoanId] = useState(null);
    const [emis, setEmis] = useState([]);
    const [isLoadingEmis, setIsLoadingEmis] = useState(false);

    const fetchLoans = async () => {
        setIsLoading(true);
        try {
            const data = await getLoans({ user_id: 1 });
            setLoans(data);
        } catch (err) {
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchLoans();
    }, []);

    const handleCreateLoan = async (e) => {
        e.preventDefault();
        try {
            await createLoan({
                user_id: 1,
                lender_name: lenderName,
                principal_amount: Number(principal),
                interest_rate: Number(interest),
                tenure_months: Number(tenure),
                start_date: startDate
            });
            setLenderName(""); setPrincipal(""); setInterest(""); setTenure(""); setStartDate("");
            fetchLoans();
        } catch (err) {
            console.error(err);
            alert("Error creating loan");
        }
    };

    const viewEmis = async (loanId) => {
        if (selectedLoanId === loanId) {
            setSelectedLoanId(null);
            return;
        }
        setSelectedLoanId(loanId);
        setIsLoadingEmis(true);
        try {
            const data = await getLoanEmis(loanId);
            setEmis(data);
        } catch (err) {
            console.error(err);
        } finally {
            setIsLoadingEmis(false);
        }
    };

    const handlePayEmi = async (emiId) => {
        try {
            await payEmi(emiId);
            viewEmis(selectedLoanId);
        } catch (err) {
            console.error(err);
            alert("Error paying EMI");
        }
    };

    return (
        <div className="dashboard-container fade-in">
            <div className="dashboard-header">
                <h2 className="dashboard-title text-gradient">Loans & EMIs</h2>
                <button className="glass-button" onClick={fetchLoans}>
                    <span style={{fontSize: "18px"}}>↻</span> Refresh
                </button>
            </div>

            <div className="dashboard-main" style={{ display: "grid", gridTemplateColumns: "1fr 2fr", gap: "20px" }}>
                <div className="transaction-section glass-panel">
                    <h3>Create New Loan</h3>
                    <form onSubmit={handleCreateLoan} style={{display: 'flex', flexDirection: 'column', gap: '15px', marginTop: '10px'}}>
                        <div className="form-group">
                            <label>Lender Name</label>
                            <input type="text" className="glass-input" value={lenderName} onChange={(e) => setLenderName(e.target.value)} required placeholder="e.g. HDFC Bank" />
                        </div>
                        <div className="form-group">
                            <label>Principal Amount (₹)</label>
                            <input type="number" className="glass-input" value={principal} onChange={(e) => setPrincipal(e.target.value)} required placeholder="e.g. 500000" />
                        </div>
                        <div className="form-group">
                            <label>Interest Rate (%)</label>
                            <input type="number" step="0.1" className="glass-input" value={interest} onChange={(e) => setInterest(e.target.value)} required placeholder="e.g. 8.5" />
                        </div>
                        <div className="form-group">
                            <label>Tenure (Months)</label>
                            <input type="number" className="glass-input" value={tenure} onChange={(e) => setTenure(e.target.value)} required placeholder="e.g. 24" />
                        </div>
                        <div className="form-group">
                            <label>Start Date</label>
                            <input type="date" className="glass-input" value={startDate} onChange={(e) => setStartDate(e.target.value)} required style={{ colorScheme: "dark" }} />
                        </div>
                        <button type="submit" className="glass-button" style={{ marginTop: '5px', width: '100%', padding: '14px' }}>
                            <span style={{fontSize: "20px", lineHeight: 1}}>+</span> Create Loan
                        </button>
                    </form>
                </div>

                <div className="chart-section glass-panel" style={{ overflowY: "auto", maxHeight: "70vh" }}>
                    <h3>Existing Loans</h3>
                    {isLoading ? <p style={{ color: "var(--text-secondary)" }}>Loading...</p> : (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px', marginTop: '20px' }}>
                            {loans.map(loan => (
                                <div key={loan.id} className="glass-panel" style={{ padding: '15px', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                        <div>
                                            <h4 style={{ margin: 0, color: 'var(--primary-color)', fontSize: '18px' }}>{loan.lender_name}</h4>
                                            <p style={{ margin: '5px 0 0', color: 'var(--text-secondary)', fontSize: '14px' }}>
                                                ₹ {loan.principal_amount?.toLocaleString()} • {loan.interest_rate}% • {loan.tenure_months} months
                                            </p>
                                        </div>
                                        <button className="glass-button" style={{ padding: '8px 15px', fontSize: '14px' }} onClick={() => viewEmis(loan.id)}>
                                            {selectedLoanId === loan.id ? 'Hide EMIs' : 'View EMIs'}
                                        </button>
                                    </div>
                                    
                                    {selectedLoanId === loan.id && (
                                        <div style={{ marginTop: '20px', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '15px' }}>
                                            <h5 style={{ margin: '0 0 10px 0', color: 'white' }}>EMI Schedule (₹ {loan.emi_amount?.toLocaleString()}/mo)</h5>
                                            {isLoadingEmis ? <p style={{ color: "var(--text-secondary)", fontSize: "14px" }}>Loading EMIs...</p> : (
                                                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: "300px", overflowY: "auto", paddingRight: "5px" }}>
                                                    {emis.map(emi => (
                                                        <div key={emi.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(0,0,0,0.2)', padding: '12px', borderRadius: '8px' }}>
                                                            <div style={{ fontSize: '13px' }}>
                                                                <div><strong style={{ color: 'white' }}>Month {emi.installment_number}</strong></div>
                                                                <div style={{ color: 'var(--text-secondary)', marginTop: '4px' }}>Due: {emi.due_date}</div>
                                                            </div>
                                                            <div>
                                                                {emi.status === 'paid' ? (
                                                                    <span style={{ color: 'var(--success-color)', fontSize: '13px', fontWeight: 'bold' }}>PAID ✓</span>
                                                                ) : (
                                                                    <button className="glass-button" style={{ padding: '6px 12px', fontSize: '13px', background: 'var(--primary-color)', color: 'white' }} onClick={() => handlePayEmi(emi.id)}>
                                                                        Pay ₹ {emi.amount.toFixed(0)}
                                                                    </button>
                                                                )}
                                                            </div>
                                                        </div>
                                                    ))}
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>
                            ))}
                            {loans.length === 0 && <p style={{ color: "var(--text-secondary)" }}>No loans found.</p>}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Loans;
