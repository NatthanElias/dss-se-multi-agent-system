/**
 * API Gateway - Central Entry Point for Microservices
 * Port: 3000
 * 
 * Routes:
 * - /auth/*  → Auth Service (http://localhost:3001)
 * - /api/*   → Agent Service (http://localhost:8080) [REQUIRES AUTH]
 * - /health  → Gateway's own health check
 * 
 * Features:
 * - Request Routing (express-http-proxy)
 * - Token Validation for /api/* routes
 * - Request Logging
 * - Error Handling
 * - CORS Configuration
 */

require('dotenv').config();
const express = require('express');
const proxy = require('express-http-proxy');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;
const AUTH_SERVICE_URL = process.env.AUTH_SERVICE_URL || 'http://localhost:3001';
const AGENT_SERVICE_URL = process.env.AGENT_SERVICE_URL || 'http://localhost:8080';

// ============================================
// Middleware
// ============================================
app.use(cors());
app.use(express.json());

// Request Logging Middleware
app.use((req, res, next) => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] ${req.method} ${req.originalUrl} → Routing...`);
    next();
});

// ============================================
// Authentication Middleware (for /api/* routes)
// ============================================
const validateToken = async (req, res, next) => {
    // Skip auth for health check
    if (req.url === '/health' || req.originalUrl.endsWith('/health')) {
        return next();
    }

    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        console.log('[Gateway] ❌ No token provided for protected route');
        return res.status(401).json({
            detail: 'Authorization token required',
            hint: 'Include header: Authorization: Bearer <token>'
        });
    }

    const token = authHeader.split(' ')[1];

    try {
        // Call Auth Service to validate token
        const response = await fetch(`${AUTH_SERVICE_URL}/auth/validate`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        const data = await response.json();

        if (!data.valid) {
            console.log('[Gateway] ❌ Invalid token');
            return res.status(401).json({
                detail: 'Invalid or expired token',
                error: data.detail || 'Token validation failed'
            });
        }

        console.log(`[Gateway] ✓ Token valid for user: ${data.user}`);
        req.user = data.user;
        next();

    } catch (error) {
        console.error('[Gateway] Auth Service unreachable:', error.message);
        return res.status(503).json({
            detail: 'Auth Service unavailable',
            error: error.message
        });
    }
};

// ============================================
// Gateway Health Check
// ============================================
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        service: 'api-gateway',
        routes: {
            auth: AUTH_SERVICE_URL,
            agent: AGENT_SERVICE_URL
        }
    });
});

// ============================================
// Proxy Routes
// ============================================

// Route /auth/* → Auth Service (NO AUTH REQUIRED)
app.use('/auth', proxy(AUTH_SERVICE_URL, {
    proxyReqPathResolver: (req) => {
        const path = '/auth' + req.url;
        console.log(`[Gateway] Routing to Auth Service: ${path}`);
        return path;
    },
    proxyErrorHandler: (err, res, next) => {
        console.error('[Gateway] Auth Service Error:', err.message);
        res.status(503).json({
            detail: 'Auth Service unavailable',
            error: err.message
        });
    }
}));

// Route /api/* → Agent Service (AUTH REQUIRED)
// First validate token, then proxy
app.use('/api', validateToken, proxy(AGENT_SERVICE_URL, {
    proxyReqPathResolver: (req) => {
        const path = '/api' + req.url;
        console.log(`[Gateway] Routing to Agent Service: ${path}`);
        return path;
    },
    proxyErrorHandler: (err, res, next) => {
        console.error('[Gateway] Agent Service Error:', err.message);
        res.status(503).json({
            detail: 'Agent Service unavailable',
            error: err.message
        });
    }
}));

// ============================================
// Fallback Routes
// ============================================

// Root endpoint
app.get('/', (req, res) => {
    res.json({
        message: 'CEMA Microservices API Gateway',
        version: '1.0.0',
        docs: 'See /health for service status',
        routes: {
            '/auth/*': 'Authentication endpoints (public)',
            '/api/*': 'Agent/Session endpoints (requires token)',
            '/health': 'Gateway health check'
        }
    });
});

// 404 Handler
app.use((req, res) => {
    console.log(`[Gateway] 404 - Route not found: ${req.method} ${req.originalUrl}`);
    res.status(404).json({
        detail: 'Route not found',
        hint: 'Use /auth/* for authentication or /api/* for agent operations'
    });
});

// Error Handler
app.use((err, req, res, next) => {
    console.error('[Gateway] Error:', err);
    res.status(500).json({ detail: 'Gateway internal error' });
});

// ============================================
// Start Server
// ============================================
app.listen(PORT, () => {
    console.log(`\n${'='.repeat(50)}`);
    console.log(`[API Gateway] Running on http://localhost:${PORT}`);
    console.log(`${'='.repeat(50)}`);
    console.log(`\nRouting Configuration:`);
    console.log(`  /auth/*  → ${AUTH_SERVICE_URL} (public)`);
    console.log(`  /api/*   → ${AGENT_SERVICE_URL} (requires auth)`);
    console.log(`  /health  → Gateway health check`);
    console.log(`\n${'='.repeat(50)}\n`);
});
