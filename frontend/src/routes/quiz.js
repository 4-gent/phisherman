import React, { useState, useEffect } from 'react'
import '../styles/quiz.css'
import fisherman from '../styles/images/fishing.png'
import fish from '../styles/images/fish1.png'
import FishHook from '../styles/images/fishHook.png'

export default function Quiz() {
    return(
        <div className='quiz-body'>
            <div className='quiz-topbar' />
            {/* <div className='water-background' /> */}
            <div className='d-flex flex-row justify-content-between'>
                <img src={fisherman} alt="fisherman" className='fisherman-image'/>
            </div>
            <img src={fish} alt="fish" className='fisherman-image'/>
            {/* backgrund image */}
            {/* fish images */}
            {/* score box */}
            <CursorFollowImage/>
        </div>
    )
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

