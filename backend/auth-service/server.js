/**
 * Auth Service - Authentication Microservice
 * Port: 3001
 * 
 * Endpoints:
 * - POST /auth/login    - Login with credentials, returns JWT
 * - GET  /auth/validate - Validate JWT token
 * - GET  /auth/health   - Health check
 * 
 * Features:
 * - JWT Authentication (jsonwebtoken)
 * - Password Hashing (bcrypt)
 * - IP Blacklist Middleware (matches Python implementation)
 * - In-memory user storage (educational purposes)
 */

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;
const JWT_SECRET = process.env.JWT_SECRET || 'super-secret-key-change-in-production';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '24h';
const BLACKLIST_FILE = process.env.BLACKLIST_FILE || 'blacklist.txt';

// ============================================
// In-Memory User Storage (Educational)
// ============================================
const users = [];

// Add default admin user (matching Python implementation)
const SALT_ROUNDS = 10;
bcrypt.hash('admin123', SALT_ROUNDS).then(hash => {
    users.push({ username: 'admin', password: hash });
    console.log('[Auth] Default admin user created');
});

// ============================================
// Middleware
// ============================================
app.use(cors());
app.use(express.json());

// Request Logging Middleware
app.use((req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
    next();
});

// IP Blacklist Middleware (matches Python implementation)
app.use((req, res, next) => {
    const clientIP = req.ip || req.connection.remoteAddress || 'unknown';
    // Normalize IPv6 localhost to IPv4
    const normalizedIP = clientIP.replace('::ffff:', '').replace('::1', '127.0.0.1');

    try {
        const blacklistPath = path.join(__dirname, BLACKLIST_FILE);
        if (fs.existsSync(blacklistPath)) {
            const content = fs.readFileSync(blacklistPath, 'utf-8');
            const blacklist = content
                .split('\n')
                .map(line => line.trim())
                .filter(line => line && !line.startsWith('#'));

            if (blacklist.includes(normalizedIP)) {
                console.warn(`[Blacklist] Blocked request from: ${normalizedIP}`);
                return res.status(403).json({ detail: 'Your IP address is banned.' });
            }
        }
    } catch (err) {
        // No blacklist file, allow all
    }

    next();
});

// ============================================
// Routes
// ============================================

// Health Check
app.get('/auth/health', (req, res) => {
    res.json({ status: 'healthy', service: 'auth-service' });
});



// Login - Returns JWT Token
app.post('/auth/login', async (req, res) => {
    try {
        const { username, password } = req.body;

        if (!username || !password) {
            return res.status(400).json({ detail: 'Username and password are required' });
        }

        // Find user
        const user = users.find(u => u.username === username);
        if (!user) {
            return res.status(401).json({
                detail: 'Incorrect username or password',
                headers: { 'WWW-Authenticate': 'Bearer' }
            });
        }

        // Verify password
        const validPassword = await bcrypt.compare(password, user.password);
        if (!validPassword) {
            return res.status(401).json({
                detail: 'Incorrect username or password',
                headers: { 'WWW-Authenticate': 'Bearer' }
            });
        }

        // Generate JWT token
        const token = jwt.sign(
            { sub: username },
            JWT_SECRET,
            { expiresIn: JWT_EXPIRES_IN }
        );

        console.log(`[Auth] User logged in: ${username}`);

        // Return in same format as Python implementation
        res.json({
            access_token: token,
            token_type: 'bearer'
        });

    } catch (error) {
        console.error('[Auth] Login error:', error);
        res.status(500).json({ detail: 'Internal server error' });
    }
});

// Validate Token
app.get('/auth/validate', (req, res) => {
    try {
        const authHeader = req.headers.authorization;

        if (!authHeader || !authHeader.startsWith('Bearer ')) {
            return res.status(401).json({
                valid: false,
                detail: 'No token provided'
            });
        }

        const token = authHeader.split(' ')[1];

        const decoded = jwt.verify(token, JWT_SECRET);
        res.json({
            valid: true,
            user: decoded.sub,
            exp: decoded.exp
        });

    } catch (error) {
        if (error.name === 'TokenExpiredError') {
            return res.status(401).json({ valid: false, detail: 'Token expired' });
        }
        if (error.name === 'JsonWebTokenError') {
            return res.status(401).json({ valid: false, detail: 'Invalid token' });
        }
        res.status(500).json({ valid: false, detail: 'Internal server error' });
    }
});

// 404 Handler
app.use((req, res) => {
    res.status(404).json({ detail: 'Not found' });
});

// Error Handler
app.use((err, req, res, next) => {
    console.error('[Auth] Error:', err);
    res.status(500).json({ detail: 'Internal server error' });
});

// ============================================
// Start Server
// ============================================
app.listen(PORT, () => {
    console.log(`[Auth Service] Running on http://localhost:${PORT}`);
    console.log(`[Auth Service] Endpoints:`);
    console.log(`  POST /auth/login    - Login with credentials`);
    console.log(`  GET  /auth/validate - Validate JWT token`);
    console.log(`  GET  /auth/health   - Health check`);
});
