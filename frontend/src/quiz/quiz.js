import React, { useState, useEffect, useRef, useCallback } from 'react';
import { createQuizSocket, setupReconnectHandler } from './socket';
import './styles.css';

/**
 * Socket-based Quiz Component
 * Mounts to #quiz-root container or fails gracefully
 */
export default function SocketQuiz({ userId, topic = 'suspicious_link', onComplete }) {
    const [socket, setSocket] = useState(null);
    const [sessionId, setSessionId] = useState(null);
    const [currentQuestion, setCurrentQuestion] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    const [isAnswerLocked, setIsAnswerLocked] = useState(false);
    const [selectedChoice, setSelectedChoice] = useState(null);
    const [feedback, setFeedback] = useState(null);
    const [progress, setProgress] = useState({ current: 0, total: 10 });
    const [score, setScore] = useState(0);
    const [timer, setTimer] = useState(null);
    const [timerSeconds, setTimerSeconds] = useState(0);
    const [completed, setCompleted] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    const answeredQids = useRef(new Set());
    const timerIntervalRef = useRef(null);

    // Initialize socket
    useEffect(() => {
        if (window.__ENABLE_QUIZ__ === false) {
            console.warn('[Quiz] Quiz disabled via window.__ENABLE_QUIZ__');
            return;
        }

        const socketInstance = createQuizSocket();
        setSocket(socketInstance);

        socketInstance.on('connect', () => {
            console.log('[Quiz] Connected to quiz namespace');
            setIsConnected(true);
            // Join quiz session
            socketInstance.emit('quiz:join', { userId, topic });
        });

        // Setup reconnect handler
        setupReconnectHandler(socketInstance, sessionId, userId, topic);

        // Quiz initialization
        socketInstance.on('quiz:init', (data) => {
            console.log('[Quiz] Initialized:', data);
            setSessionId(data.sessionId);
            setProgress({ current: 0, total: data.totalQuestions || 10 });

            // Analytics hook
            if (window.__quiz_onEvent) {
                window.__quiz_onEvent('init', data);
            }
        });

        // Receive question
        socketInstance.on('quiz:question', (data) => {
            console.log('[Quiz] Question received:', data);

            // Idempotency check
            if (answeredQids.current.has(data.qid)) {
                console.warn('[Quiz] Ignoring duplicate question:', data.qid);
                return;
            }

            setCurrentQuestion(data);
            setIsAnswerLocked(false);
            setSelectedChoice(null);
            setFeedback(null);
            setProgress(prev => ({ ...prev, current: data.index + 1 }));

            // Start timer if provided
            if (data.seconds) {
                setTimerSeconds(data.seconds);
                setTimer(data.seconds);

                // Clear existing timer
                if (timerIntervalRef.current) {
                    clearInterval(timerIntervalRef.current);
                }

                // Start countdown
                timerIntervalRef.current = setInterval(() => {
                    setTimerSeconds(prev => {
                        if (prev <= 1) {
                            clearInterval(timerIntervalRef.current);
                            // Auto-submit as "no answer" (index -1)
                            handleAnswerSubmit(-1, data.qid);
                            return 0;
                        }
                        return prev - 1;
                    });
                }, 1000);
            }

            // Analytics hook
            if (window.__quiz_onEvent) {
                window.__quiz_onEvent('question', data);
            }
        });

        // Score update
        socketInstance.on('quiz:score:update', (data) => {
            console.log('[Quiz] Score update:', data);
            setScore(data.total);
            setFeedback({
                qid: data.qid,
                correct: data.correct,
                delta: data.delta
            });

            // Analytics hook
            if (window.__quiz_onEvent) {
                window.__quiz_onEvent('score', data);
            }
        });

        // Quiz complete
        socketInstance.on('quiz:complete', (data) => {
            console.log('[Quiz] Complete:', data);
            setCompleted(true);
            setResults(data);
            setIsAnswerLocked(true);

            if (timerIntervalRef.current) {
                clearInterval(timerIntervalRef.current);
            }

            // Analytics hook
            if (window.__quiz_onEvent) {
                window.__quiz_onEvent('complete', data);
            }

            if (onComplete) {
                onComplete(data);
            }
        });

        // Error handling
        socketInstance.on('quiz:error', (data) => {
            console.error('[Quiz] Error:', data);
            setError(data.message || 'An error occurred');
        });

        // Cleanup
        return () => {
            if (timerIntervalRef.current) {
                clearInterval(timerIntervalRef.current);
            }
            if (socketInstance && socketInstance.connected) {
                socketInstance.emit('quiz:leave', { sessionId });
                socketInstance.disconnect();
            }
        };
    }, [userId, topic, sessionId, onComplete]);

    // Handle answer selection
    const handleAnswerSelect = useCallback((choiceIndex) => {
        if (isAnswerLocked || completed || !currentQuestion) return;
        setSelectedChoice(choiceIndex);
    }, [isAnswerLocked, completed, currentQuestion]);

    // Handle answer submission
    const handleAnswerSubmit = useCallback((choiceIndex, qid = null) => {
        if (isAnswerLocked || completed || !currentQuestion || !socket) return;

        const questionQid = qid || currentQuestion.qid;
        let finalChoice = choiceIndex !== null ? choiceIndex : selectedChoice;

        if (finalChoice === null && choiceIndex === -1) {
            // Timer expired, no answer
            finalChoice = -1;
        }

        if (finalChoice === null) return;

        // Lock answer
        setIsAnswerLocked(true);
        answeredQids.current.add(questionQid);

        // Clear timer
        if (timerIntervalRef.current) {
            clearInterval(timerIntervalRef.current);
            setTimer(null);
            setTimerSeconds(0);
        }

        // Send answer
        socket.emit('quiz:answer', {
            sessionId,
            qid: questionQid,
            choiceIndex: finalChoice
        });

        // Analytics hook
        if (window.__quiz_onEvent) {
            window.__quiz_onEvent('answer', {
                qid: questionQid,
                choiceIndex: finalChoice
            });
        }

        // Auto-request next question after a short delay
        setTimeout(() => {
            if (!completed && socket) {
                socket.emit('quiz:next', { sessionId });
            }
        }, 2000);
    }, [isAnswerLocked, completed, currentQuestion, socket, sessionId, selectedChoice]);

    // Keyboard navigation
    useEffect(() => {
        if (!currentQuestion || isAnswerLocked || completed) return;

        const handleKeyPress = (e) => {
            if (e.key === 'Enter' && selectedChoice !== null) {
                handleAnswerSubmit(null);
            } else if (e.key >= '1' && e.key <= '9') {
                const index = parseInt(e.key) - 1;
                if (index < currentQuestion.options.length) {
                    handleAnswerSelect(index);
                }
            } else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                e.preventDefault();
                if (selectedChoice === null) {
                    handleAnswerSelect(0);
                } else {
                    const next = e.key === 'ArrowDown'
                        ? Math.min(selectedChoice + 1, currentQuestion.options.length - 1)
                        : Math.max(selectedChoice - 1, 0);
                    handleAnswerSelect(next);
                }
            }
        };

        window.addEventListener('keydown', handleKeyPress);
        return () => window.removeEventListener('keydown', handleKeyPress);
    }, [currentQuestion, selectedChoice, isAnswerLocked, completed, handleAnswerSelect, handleAnswerSubmit]);

    // Render quiz UI
    if (!isConnected) {
        return (
            <div className="quiz-loading">
                <p>Connecting to quiz server...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="quiz-error">
                <p>Error: {error}</p>
            </div>
        );
    }

    if (completed && results) {
        return (
            <div className="quiz-complete">
                <h2>Quiz Complete!</h2>
                <div className="quiz-results">
                    <p><strong>Total Score:</strong> {results.total}</p>
                    <p><strong>Correct:</strong> {results.correctCount}</p>
                    <p><strong>Wrong:</strong> {results.wrongCount}</p>
                </div>
            </div>
        );
    }

    if (!currentQuestion) {
        return (
            <div className="quiz-loading">
                <p>Waiting for first question...</p>
            </div>
        );
    }

    return (
        <div className="socket-quiz-container">
            {/* Progress indicator */}
            <div className="quiz-progress">
                <span>Q {progress.current}/{progress.total}</span>
                {timer !== null && (
                    <span className="quiz-timer">⏱ {timerSeconds}s</span>
                )}
            </div>

            {/* Question */}
            <div className="quiz-question-text">
                {currentQuestion.text}
            </div>

            {/* Options */}
            <div className="quiz-options">
                {currentQuestion.options.map((option, index) => {
                    const isSelected = selectedChoice === index;
                    const isLocked = isAnswerLocked;
                    const showFeedback = feedback && feedback.qid === currentQuestion.qid;
                    const isCorrect = showFeedback && feedback.correct && currentQuestion.answer_index === index;
                    const isWrong = showFeedback && !feedback.correct && isSelected;

                    return (
                        <button
                            key={index}
                            className={`quiz-option ${isSelected ? 'selected' : ''} ${isLocked ? 'locked' : ''} ${isCorrect ? 'correct' : ''} ${isWrong ? 'wrong' : ''}`}
                            onClick={() => {
                                if (!isLocked) {
                                    handleAnswerSelect(index);
                                    handleAnswerSubmit(index);
                                }
                            }}
                            disabled={isLocked}
                            aria-pressed={isSelected}
                        >
                            <span className="option-number">{index + 1}</span>
                            <span className="option-text">{option}</span>
                            {showFeedback && (
                                <span className="option-feedback">
                                    {isCorrect ? '✓' : isWrong ? '✗' : ''}
                                </span>
                            )}
                        </button>
                    );
                })}
            </div>

            {/* Score badge */}
            <div className="quiz-score-badge">
                Score: {score}
            </div>
        </div>
    );
}

/**
 * Mount function for #quiz-root container
 */
export function mountQuiz(options = {}) {
    const {
        userId = 'anonymous',
        topic = 'suspicious_link',
        onComplete = null
    } = options;

    const container = document.getElementById('quiz-root');
    if (!container) {
        console.warn('[Quiz] Container #quiz-root not found. Quiz will not mount.');
        return null;
    }

    // For React mounting, this would typically be called from quiz.js route
    // Return component props instead
    return { userId, topic, onComplete };
}

