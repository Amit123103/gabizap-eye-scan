import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        if (token) {
            // In production: Validate token with backend
            setIsAuthenticated(true);
        }
    }, [token]);

    const login = async (email, password) => {
        // DEMO MODE: Accept admin@gabizap.io with any password
        // In production, this would call the backend API
        if (email === 'admin@gabizap.io' || (email === 'admin@example.com' && password === 'admin')) {
            const mockToken = 'demo_token_' + Date.now();
            localStorage.setItem('token', mockToken);
            setToken(mockToken);
            setIsAuthenticated(true);
            return true;
        }
        return false;
    };

    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{ user, token, isAuthenticated, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
