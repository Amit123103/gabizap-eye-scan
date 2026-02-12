import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
    base: '/gabizap-eye-scan/',
    server: {
        port: 3001
    }
})
