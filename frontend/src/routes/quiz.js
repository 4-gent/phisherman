import React, { useState, useEffect, useRef } from 'react'
import '../styles/quiz.css'
import fisherman from '../styles/images/fishing.png'
import fish from '../styles/images/fish1.png'
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
        const pixelAnchor = { x: 787, y: 233 };

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

    return(
        <div className='quiz-scene'>
            {/* small centered box inside the scene */}
            <div className='white-box' />
            {/* top-right trackers: correct answers and score */}
            <div className='top-right-panel'>
                <div className='tracker-box correct-box'>
                    <div className='tracker-label'>Correct</div>
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
                />
            </div>
                <img src={FishA} alt="fish" className='fishiesA'/>
                <img src={FishB} alt="fish" className='fishiesB'/>
                <img src={FishC} alt="fish" className='fishiesC'/>
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

    const followerStyle = {
        position: 'fixed',
        top: mousePosition.y,
        left: mousePosition.x,
    }


    const svgStyle = {
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        pointerEvents: 'none',
    }

    return (
        <div className="quiz-container">
            <img
                src={FishHook}
                alt="fish hook"
                style={followerStyle}
                className="cursor-follower"
            />
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

