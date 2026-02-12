import React, { useRef, useEffect, useState } from 'react';
import { Box, Typography, Button, LinearProgress } from '@mui/material';

const BiometricScanner = ({ onScanComplete, type = "iris" }) => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [scanning, setScanning] = useState(false);
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        startCamera();
        return () => stopCamera();
    }, []);

    const startCamera = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }
        } catch (err) {
            console.error("Camera access denied:", err);
        }
    };

    const stopCamera = () => {
        if (videoRef.current && videoRef.current.srcObject) {
            videoRef.current.srcObject.getTracks().forEach(track => track.stop());
        }
    };

    const handleScan = () => {
        setScanning(true);
        setProgress(0);

        // Simulate scanning process
        const interval = setInterval(() => {
            setProgress(old => {
                if (old >= 100) {
                    clearInterval(interval);
                    captureAndSend();
                    return 100;
                }
                return old + 5;
            });
        }, 100);
    };

    const captureAndSend = () => {
        if (!videoRef.current || !canvasRef.current) return;

        const context = canvasRef.current.getContext('2d');
        context.drawImage(videoRef.current, 0, 0, 320, 240);

        canvasRef.current.toBlob(async (blob) => {
            // Send to backend
            const formData = new FormData();
            formData.append('file', blob);

            try {
                // For demo, we mock the response
                // In production, would send to: type === 'iris' ? '/iris/embed' : '/hand/process'
                onScanComplete({ success: true, biometrics: "mock_data" });
            } catch (e) {
                onScanComplete({ success: false, error: e.message });
            }
            setScanning(false);
        }, 'image/jpeg');
    };

    return (
        <Box sx={{ position: 'relative', width: 320, height: 240, bgcolor: 'black', overflow: 'hidden', borderRadius: 2 }}>
            <video ref={videoRef} autoPlay playsInline style={{ width: '100%', height: '100%', objectFit: 'cover', opacity: scanning ? 0.5 : 1 }} />
            <canvas ref={canvasRef} width="320" height="240" style={{ display: 'none' }} />

            {/* Overlay UI */}
            <Box sx={{
                position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, border: '2px solid cyan', borderRadius: 2, pointerEvents: 'none',
                boxShadow: scanning ? 'inset 0 0 50px cyan' : 'none', transition: 'box-shadow 0.3s'
            }} />

            {scanning && (
                <Box sx={{ position: 'absolute', bottom: 10, left: 10, right: 10 }}>
                    <Typography variant="caption" color="cyan" sx={{ textShadow: '0 0 5px cyan' }}>SCANNING...</Typography>
                    <LinearProgress variant="determinate" value={progress} color="primary" />
                </Box>
            )}

            {!scanning && (
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleScan}
                    sx={{ position: 'absolute', bottom: 20, left: '50%', transform: 'translateX(-50%)' }}
                >
                    START SCAN
                </Button>
            )}
        </Box>
    );
};

export default BiometricScanner;
