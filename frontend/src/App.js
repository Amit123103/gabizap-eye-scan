import React, { useState } from 'react';
import { ThemeProvider, createTheme, CssBaseline, Container, Box, Typography, Button, Alert } from '@mui/material';
import { AuthProvider, useAuth } from './AuthContext';
import BiometricScanner from './components/BiometricScanner';
import AdminDashboard from './components/AdminDashboard';

const darkTheme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#00e5ff',
        },
        secondary: {
            main: '#ff2d55',
        },
        background: {
            default: '#0a1929',
            paper: '#132f4c',
        },
    },
    typography: {
        fontFamily: '"Roboto Mono", "Helvetica", "Arial", sans-serif',
    },
});

function LoginPanel() {
    const { login } = useAuth();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleLogin = async () => {
        const success = await login(email, password);
        if (!success) setError("Authentication Failed");
    };

    return (
        <Box sx={{ p: 4, border: '1px solid #333', borderRadius: 2, bgcolor: 'background.paper', width: '100%', maxWidth: 400, textAlign: 'center' }}>
            <Typography variant="h5" gutterBottom color="primary">SECURE LOGIN</Typography>
            {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

            <input
                type="text"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                style={{ width: '100%', padding: '10px', marginBottom: '10px', background: '#0a1929', border: '1px solid #333', color: 'white' }}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{ width: '100%', padding: '10px', marginBottom: '20px', background: '#0a1929', border: '1px solid #333', color: 'white' }}
            />
            <Button variant="contained" fullWidth onClick={handleLogin}>AUTHENTICATE</Button>
        </Box>
    );
}

function Dashboard() {
    const { logout } = useAuth();
    const [scanResult, setScanResult] = useState(null);

    const handleScan = (result) => {
        setScanResult(result);
    };

    return (
        <Box sx={{ width: '100%' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
                <Typography variant="h4" color="primary">COMMAND CENTER</Typography>
                <Button variant="outlined" color="error" onClick={logout}>LOGOUT</Button>
            </Box>

            <Box sx={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                <Box>
                    <Typography variant="h6" gutterBottom>Biometric Verification</Typography>
                    <BiometricScanner onScanComplete={handleScan} />
                    {scanResult && (
                        <Alert severity={scanResult.success ? "success" : "error"} sx={{ mt: 2 }}>
                            {scanResult.success ? "IDENTITY CONFIRMED" : "ACCESS DENIED"}
                        </Alert>
                    )}
                </Box>

                <Box sx={{ flex: 1, p: 3, border: '1px solid #333', borderRadius: 2 }}>
                    <Typography variant="h6" gutterBottom>System Status</Typography>
                    <Typography>Zero Trust: <span style={{ color: '#0f0' }}>ACTIVE</span></Typography>
                    <Typography>Risk Level: <span style={{ color: '#0f0' }}>LOW (12%)</span></Typography>
                </Box>
            </Box>
        </Box>
    );
}

function AppContent() {
    const { isAuthenticated } = useAuth();
    // Simple toggle for demo purposes, in real app use Router
    const [view, setView] = useState('user');

    return (
        <Container maxWidth="xl">
            <Box sx={{ my: 4, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%', mb: 2, px: 4 }}>
                    <Typography variant="h2" component="h1" sx={{ fontWeight: 'bold', letterSpacing: '0.1em' }} color="primary">
                        GABIZAP
                    </Typography>
                    {isAuthenticated && (
                        <Button onClick={() => setView(view === 'user' ? 'admin' : 'user')} variant="outlined">
                            SWITCH TO {view === 'user' ? 'ADMIN' : 'USER'} VIEW
                        </Button>
                    )}
                </Box>

                <Typography variant="caption" sx={{ mb: 6 }} color="text.secondary">
                    V 1.0.0 | MIL-SPEC SECURITY | ZERO TRUST
                </Typography>

                {isAuthenticated ? (
                    view === 'admin' ? <AdminDashboard /> : <Dashboard />
                ) : (
                    <LoginPanel />
                )}
            </Box>
        </Container>
    );
}

function App() {
    return (
        <ThemeProvider theme={darkTheme}>
            <CssBaseline />
            <AuthProvider>
                <AppContent />
            </AuthProvider>
        </ThemeProvider>
    );
}

export default App;
