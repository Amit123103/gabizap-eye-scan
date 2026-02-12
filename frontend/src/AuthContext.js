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
        try {
            const API_URL = import.meta.env.VITE_API_URL || 'https://gabizap-eye-scan.onrender.com';
            const response = await fetch(`${API_URL}/auth/token`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            const newToken = data.access_token;

            localStorage.setItem('token', newToken);
            setToken(newToken);
            setIsAuthenticated(true);
            return true;
        } catch (error) {
            console.error("Login error:", error);
            return false;
        }
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
