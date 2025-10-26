import io from 'socket.io-client';

/**
 * Socket factory for quiz namespace
 * Reads socket URL from window.__WS_URL__ or defaults to same-origin
 */
export function createQuizSocket() {
    // Default to backend server (port 8080) if no explicit URL set
    const wsUrl = window.__WS_URL__ || 'http://localhost:8080';
    const socket = io(`${wsUrl}/quiz`, {
        transports: ['polling', 'websocket'], // Try polling first for better compatibility
        reconnection: true,
        reconnectionDelay: 2000,
        reconnectionDelayMax: 10000,
        reconnectionAttempts: 10,
        timeout: 20000,
        forceNew: false, // Reuse existing connection if available
    });

    return socket;
}

/**
 * Reconnect handler - sends quiz:join with sessionId to resume state
 */
export function setupReconnectHandler(socket, sessionId, userId, topic) {
    socket.on('reconnect', () => {
        console.log('[Quiz] Socket reconnected, resuming session:', sessionId);
        if (sessionId) {
            socket.emit('quiz:join', { userId, topic, sessionId });
        } else {
            socket.emit('quiz:join', { userId, topic });
        }
    });

    socket.on('disconnect', () => {
        console.log('[Quiz] Socket disconnected');
    });

    socket.on('connect_error', (error) => {
        console.error('[Quiz] Connection error:', error);
    });
}

