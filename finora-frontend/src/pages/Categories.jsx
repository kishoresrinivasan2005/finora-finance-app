import { useEffect, useState } from "react";
import { getCategories, createCategory } from "../api/services";

function Categories() {
    const [categories, setCategories] = useState([]);
    const [name, setName] = useState("");
    const [isLoading, setIsLoading] = useState(true);

    const fetchCategories = async () => {
        setIsLoading(true);
        try {
            const data = await getCategories();
            setCategories(data);
        } catch (err) {
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchCategories();
    }, []);

    const handleAddCategory = async (e) => {
        e.preventDefault();
        if (!name.trim()) return;
        try {
            await createCategory({ name });
            setName("");
            fetchCategories();
        } catch (err) {
            console.error(err);
            alert("Error creating category. It might already exist.");
        }
    };

    return (
        <div className="dashboard-container fade-in">
            <div className="dashboard-header">
                <h2 className="dashboard-title text-gradient">Categories</h2>
                <button className="glass-button" onClick={fetchCategories}>
                    <span style={{fontSize: "18px"}}>↻</span> Refresh
                </button>
            </div>
            <div className="dashboard-main" style={{ display: "grid", gridTemplateColumns: "1fr 2fr", gap: "20px" }}>
                <div className="transaction-section glass-panel">
                    <h3>Add New Category</h3>
                    <form onSubmit={handleAddCategory} style={{display: 'flex', flexDirection: 'column', gap: '20px', marginTop: '10px'}}>
                        <div className="form-group">
                            <label>Category Name</label>
                            <input 
                                type="text" 
                                className="glass-input" 
                                placeholder="e.g. Travel" 
                                value={name} 
                                onChange={(e) => setName(e.target.value)} 
                                required 
                            />
                        </div>
                        <button type="submit" className="glass-button" style={{ marginTop: '16px', width: '100%', padding: '14px' }}>
                            <span style={{fontSize: "20px", lineHeight: 1}}>+</span> Add Category
                        </button>
                    </form>
                </div>
                <div className="chart-section glass-panel">
                    <h3>Existing Categories</h3>
                    {isLoading ? <p style={{ color: "var(--text-secondary)" }}>Loading...</p> : (
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '15px', marginTop: '20px' }}>
                            {categories.map(cat => (
                                <div key={cat.id} className="glass-panel" style={{ padding: '12px 24px', borderRadius: '30px', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)' }}>
                                    {cat.name}
                                </div>
                            ))}
                            {categories.length === 0 && <p style={{ color: "var(--text-secondary)" }}>No categories found.</p>}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Categories;
