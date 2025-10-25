import React, { useState, useEffect } from 'react'
import '../styles/quiz.css'
import FishHook from '../styles/images/fishHook.png';

export default function Quiz() {
    return <CursorFollowImage />;
}

function CursorFollowImage() {
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
        left: mousePosition.x,
        top: mousePosition.y,
        pointerEvents: 'none',
        transform: 'translate(-50%, -50%)',
    };

    return (
        <div className="quiz-container">
            <img
                src={FishHook}
                alt="fish hook"
                style={followerStyle}
                className="cursor-follower"
            />
        </div>
    );
}

