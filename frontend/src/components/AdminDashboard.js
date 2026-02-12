import React from 'react';
import { Box, Typography, Grid, Paper, Table, TableBody, TableCell, TableHead, TableRow, Chip } from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';

const dataRisk = [
    { name: '00:00', risk: 12 },
    { name: '04:00', risk: 8 },
    { name: '08:00', risk: 45 },
    { name: '12:00', risk: 30 },
    { name: '16:00', risk: 65 },
    { name: '20:00', risk: 25 },
];

const dataAuth = [
    { name: 'Mon', success: 400, fail: 24 },
    { name: 'Tue', success: 300, fail: 13 },
    { name: 'Wed', success: 550, fail: 58 },
    { name: 'Thu', success: 480, fail: 35 },
    { name: 'Fri', success: 600, fail: 40 },
];

const mockAuditLogs = [
    { id: 1, user: 'admin', action: 'SYSTEM_STARTUP', time: '2026-02-12 08:00:01', risk: 'LOW' },
    { id: 2, user: 'u_1023', action: 'LOGIN_ATTEMPT', time: '2026-02-12 08:05:22', risk: 'MEDIUM' },
    { id: 3, user: 'u_9999', action: 'IRIS_SCAN_FAIL', time: '2026-02-12 08:15:00', risk: 'HIGH' },
    { id: 4, user: 'u_1023', action: 'LOGIN_SUCCESS', time: '2026-02-12 08:15:10', risk: 'LOW' },
];

const AdminDashboard = () => {
    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" color="primary" gutterBottom>SECURITY OPERATIONS CENTER</Typography>

            <Grid container spacing={3}>
                {/* Stats Cards */}
                <Grid item xs={12} md={3}>
                    <Paper sx={{ p: 2, bgcolor: 'background.paper', border: '1px solid #333' }}>
                        <Typography variant="subtitle2" color="text.secondary">Active Sessions</Typography>
                        <Typography variant="h3" color="white">1,248</Typography>
                    </Paper>
                </Grid>
                <Grid item xs={12} md={3}>
                    <Paper sx={{ p: 2, bgcolor: 'background.paper', border: '1px solid #333' }}>
                        <Typography variant="subtitle2" color="text.secondary">Threat Level</Typography>
                        <Typography variant="h3" color="error">ELEVATED</Typography>
                    </Paper>
                </Grid>
                <Grid item xs={12} md={3}>
                    <Paper sx={{ p: 2, bgcolor: 'background.paper', border: '1px solid #333' }}>
                        <Typography variant="subtitle2" color="text.secondary">Biometric Matches (24h)</Typography>
                        <Typography variant="h3" color="primary">99.9%</Typography>
                    </Paper>
                </Grid>
                <Grid item xs={12} md={3}>
                    <Paper sx={{ p: 2, bgcolor: 'background.paper', border: '1px solid #333' }}>
                        <Typography variant="subtitle2" color="text.secondary">Blocked IPs</Typography>
                        <Typography variant="h3" color="warning.main">42</Typography>
                    </Paper>
                </Grid>

                {/* Charts */}
                <Grid item xs={12} md={8}>
                    <Paper sx={{ p: 2, bgcolor: 'background.paper', border: '1px solid #333', height: 350 }}>
                        <Typography variant="h6" gutterBottom>Authentication Traffic</Typography>
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={dataAuth}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                                <XAxis dataKey="name" stroke="#888" />
                                <YAxis stroke="#888" />
                                <Tooltip contentStyle={{ backgroundColor: '#132f4c', borderColor: '#333' }} />
                                <Legend />
                                <Bar dataKey="success" fill="#00e5ff" name="Success" />
                                <Bar dataKey="fail" fill="#ff2d55" name="Failed" />
                            </BarChart>
                        </ResponsiveContainer>
                    </Paper>
                </Grid>
                <Grid item xs={12} md={4}>
                    <Paper sx={{ p: 2, bgcolor: 'background.paper', border: '1px solid #333', height: 350 }}>
                        <Typography variant="h6" gutterBottom>Real-time Risk Score</Typography>
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={dataRisk}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                                <XAxis dataKey="name" stroke="#888" />
                                <YAxis domain={[0, 100]} stroke="#888" />
                                <Tooltip contentStyle={{ backgroundColor: '#132f4c', borderColor: '#333' }} />
                                <Line type="monotone" dataKey="risk" stroke="#ffca28" strokeWidth={3} dot={{ r: 4 }} />
                            </LineChart>
                        </ResponsiveContainer>
                    </Paper>
                </Grid>

                {/* Audit Log Table */}
                <Grid item xs={12}>
                    <Paper sx={{ p: 2, bgcolor: 'background.paper', border: '1px solid #333' }}>
                        <Typography variant="h6" gutterBottom>Forensic Audit Stream</Typography>
                        <Table size="small">
                            <TableHead>
                                <TableRow>
                                    <TableCell sx={{ color: '#888' }}>Timestamp</TableCell>
                                    <TableCell sx={{ color: '#888' }}>User</TableCell>
                                    <TableCell sx={{ color: '#888' }}>Action</TableCell>
                                    <TableCell sx={{ color: '#888' }}>Risk Assessment</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {mockAuditLogs.map((row) => (
                                    <TableRow key={row.id}>
                                        <TableCell sx={{ color: 'white' }}>{row.time}</TableCell>
                                        <TableCell sx={{ color: 'white' }}>{row.user}</TableCell>
                                        <TableCell sx={{ color: 'white' }}>{row.action}</TableCell>
                                        <TableCell>
                                            <Chip
                                                label={row.risk}
                                                size="small"
                                                color={row.risk === 'HIGH' ? 'error' : row.risk === 'MEDIUM' ? 'warning' : 'success'}
                                            />
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
};

export default AdminDashboard;
