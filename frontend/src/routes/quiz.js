import React, { useState, useEffect, useRef } from 'react'
import '../styles/quiz.css'
import fisherman from '../styles/images/fishing1.png'
import FishHook from '../styles/images/fishHook.png'
import FishA from '../styles/images/fishA.png'
import FishB from '../styles/images/fishB.png'
import FishC from '../styles/images/fishC.png'

export default function Quiz() {
    const fishermanRef = useRef(null);
    const [anchor, setAnchor] = useState({ x: 100, y: 100 });
    
    // added function to compute anchor from fisherman image
    const updateAnchorFromImage = () => {
        const el = fishermanRef.current;
        if (!el) return;
        const rect = el.getBoundingClientRect();

        // pixel coordinates in the source image where you want the anchor (adjust as needed)
        const pixelAnchor = { x: 786, y: 233 };

        // use natural image size if available to map pixels to rendered size
        const naturalW = el.naturalWidth || rect.width;
        const naturalH = el.naturalHeight || rect.height;

        const anchorX = rect.left + (pixelAnchor.x / naturalW) * rect.width;
        const anchorY = rect.top + (pixelAnchor.y / naturalH) * rect.height;

        setAnchor({ 
            x: Math.round(anchorX), 
            y: Math.round(anchorY) 
        });
    };

    useEffect(() => {
        updateAnchorFromImage()
        window.addEventListener('resize', updateAnchorFromImage)
        return () => window.removeEventListener('resize', updateAnchorFromImage)

    }, [])

    // quiz counters
    const totalQuestions = 10;
    const [correctCount, setCorrectCount] = useState(0);
    const [score, setScore] = useState(0);

    const [selected, setSelected] = useState({});

    const toggleSelect = (key) => {
        setSelected(prev => ({ ...prev, [key]: !prev[key] }));
    };

    const handleKeySelect = (e, key) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            toggleSelect(key);
        }
    };

    // fish A play/stop state and timers
    const [fishAState, setFishAState] = useState('playing'); // 'playing' | 'stopped'
    const initialStopTimer = useRef(null);
    const resumeTimer = useRef(null);

    const finishTimerRef = useRef(null);

    useEffect(() => {
        // start in playing1 immediately
        setFishAState('playing1');

        // after 5s switch to stopped, then auto-resume to playing2 after 25s
        initialStopTimer.current = setTimeout(() => {
            setFishAState('stopped');
            initialStopTimer.current = null;

            resumeTimer.current = setTimeout(() => {
                resumeTimer.current = null;
                setFishAState('playing2');

                // when playing2 finishes after 5s, mark finished (or set any state you prefer)
                finishTimerRef.current = setTimeout(() => {
                    setFishAState('finished');
                    finishTimerRef.current = null;
                }, 5000);
            }, 25000); // 25s stopped period
        }, 5000); // 5s playing1 period

        return () => {
            if (initialStopTimer.current) {
                clearTimeout(initialStopTimer.current);
                initialStopTimer.current = null;
            }
            if (resumeTimer.current) {
                clearTimeout(resumeTimer.current);
                resumeTimer.current = null;
            }
            if (finishTimerRef.current) {
                clearTimeout(finishTimerRef.current);
                finishTimerRef.current = null;
            }
        };
    }, []);

    const handleSendClick = () => {
        // If currently stopped, cancel auto-resume and start playing2 immediately
        if (fishAState === 'stopped') {
            if (resumeTimer.current) {
                clearTimeout(resumeTimer.current);
                resumeTimer.current = null;
            }
            setFishAState('playing2');

            // start the playing2 finish timer (5s) if not already running
            if (finishTimerRef.current) {
                clearTimeout(finishTimerRef.current);
                finishTimerRef.current = null;
            }
            finishTimerRef.current = setTimeout(() => {
                setFishAState('finished');
                finishTimerRef.current = null;
            }, 5000);
        }
    };

    return(

        <div className='quiz-scene'>
            {/* small centered box inside the scene */}
            <div className='white-box'>
                <div className='inner-white-box'>
                    <h2 className='quiz-question'>Which of these fish is a Phishing attempt?</h2>
                    <p className='quiz-instructions'>Click on a fish to select your answer.</p>
                </div>

            </div>
            {/* top-right trackers: correct answers and score */}
            <div className='top-right-panel'>
                <div className='tracker-box correct-box'>
                    <div className='tracker-label'>Questions</div>
                    <div className='tracker-value'>{correctCount} / {totalQuestions}</div>
                </div>
                <div className='tracker-box score-box'>
                    <div className='tracker-label'>Score</div>
                    <div className='tracker-value'>{score}</div>
                </div>
            </div>

        <div className='quiz-body'>
            <div className='quiz-midbar' />
            {/* <div className='water-background' /> */}
            <div className='d-flex flex-row justify-content-between'>
                <img 
                    src={fisherman}
                    ref={fishermanRef} 
                    alt="fisherman" 
                    className='fisherman-image'
                    onLoad={updateAnchorFromImage}
                    draggable={false}
                    onDragStart={(e) => e.preventDefault()}
                />
            </div>
                    <button
                        type="button"
                        className={`fishiesA ${fishAState} selectable ${selected.fishA ? 'selected' : ''}`}
                        onClick={() => toggleSelect('fishA')}
                        aria-pressed={!!selected.fishA}
                        onKeyDown={(e) => handleKeySelect(e, 'fishA')}
                    >
                        {selected.fishA ? 'Fish A (selected)' : 'Fish A'} {/* this is where you put the text */}
                    </button>

                    <button
                        type="button"
                        className={`fishiesB ${fishAState} selectable ${selected.fishB ? 'selected' : ''}`}
                        onClick={() => toggleSelect('fishB')}
                        aria-pressed={!!selected.fishB}
                        onKeyDown={(e) => handleKeySelect(e, 'fishB')}
                    >
                        {selected.fishB ? 'Fish B (selected)' : 'Fish B'} {/* this is where you put the text */}
                    </button>

                    <button
                        type="button"
                        className={`fishiesC ${fishAState} selectable ${selected.fishC ? 'selected' : ''}`}
                        onClick={() => toggleSelect('fishC')}
                        aria-pressed={!!selected.fishC}
                        onKeyDown={(e) => handleKeySelect(e, 'fishC')}
                    >
                        {selected.fishC ? 'Fish C (selected)' : 'Fish C'} {/* this is where you put the text */}
                    </button>
            </div>
            
            <CursorFollowImage anchor={anchor} />
        </div>
    )
}

function CursorFollowImage({ anchor }) {
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

    useEffect(() => {
        const handleMouseMove = (event) => {
            setMousePosition({ x: event.clientX, y: event.clientY });
        };

        window.addEventListener('mousemove', handleMouseMove);
        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
        };
    }, []);

    const svgStyle = {
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        pointerEvents: 'none',
        zIndex: 2
    }

    return (
        <div className="quiz-container">
            <svg style={svgStyle}>
                <line
                    x1={mousePosition.x}
                    y1={mousePosition.y}
                    x2={anchor.x}
                    y2={anchor.y}
                    stroke="#000"
                    strokeWidth="1"
                />
            </svg>
        </div>
    );
}

