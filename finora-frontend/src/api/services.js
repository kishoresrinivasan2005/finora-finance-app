import api from './axios';

// ==========================================
// TRANSACTIONS
// ==========================================
export const getTransactions = async (params = {}) => {
    const response = await api.get('/transactions/', { params });
    return response.data;
};

export const createTransaction = async (data) => {
    const response = await api.post('/transactions/', data);
    return response.data;
};

export const getTransactionsSummary = async (path, params = {}) => {
    // path can be 'current-month', 'monthly-expense-trend', etc.
    const response = await api.get(`/transactions/summary/${path}`, { params });
    return response.data;
};

// ==========================================
// CATEGORIES
// ==========================================
export const getCategories = async () => {
    const response = await api.get('/categories/');
    return response.data;
};

export const createCategory = async (data) => {
    const response = await api.post('/categories/', data);
    return response.data;
};

export const getCategoryTransactions = async (categoryId) => {
    const response = await api.get(`/categories/${categoryId}/transactions`);
    return response.data;
};

// ==========================================
// LOANS & EMIs
// ==========================================
export const getLoans = async (params = {}) => {
    const response = await api.get('/loans/', { params });
    return response.data;
};

export const createLoan = async (data) => {
    const response = await api.post('/loans/', data);
    return response.data;
};

export const getLoanEmis = async (loanId) => {
    const response = await api.get(`/loans/${loanId}/emis`);
    return response.data;
};

export const payEmi = async (emiId) => {
    const response = await api.patch(`/emis/${emiId}/pay`);
    return response.data;
};
