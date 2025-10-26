import React, { useState, useEffect } from 'react'
import '../styles/trainer.css'
import '../styles/loading.css'
import { io } from "socket.io-client";
import { FaSpinner } from "react-icons/fa"
import axios from 'axios';

import wave2 from '../styles/images/support_images/wave2.svg'
import UserNav from '../components/usernavbar';

export default function Trainer() {
    // State following the contract structure
    const [concepts, setConcepts] = useState({
        1: { loading: true, title: '', points: [] },
        2: { loading: true, title: '', points: [] },
        3: { loading: true, title: '', points: [] }
    })

    useEffect(() => {
        const socket = io('http://localhost:8080', { withCredentials: true })

        socket.on('connect', () => {
            socket.emit('join_training', { room: 'personal' })
        })

        socket.on('concept_update', (msg) => {
            const { concept, title, points } = msg || {}

            if (concept && (concept === 1 || concept === 2 || concept === 3)) {
                setConcepts(prev => ({
                    ...prev,
                    [concept]: {
                        loading: false,
                        title: title || '',
                        points: points || []
                    }
                }))
            }
        })

        return () => {
            socket.disconnect()
        }
    }, [])

    const handleTraining = async (training) => {
        try {
            const response = await axios.post('http://localhost:8080/api/completion', { training }, { withCredentials: true })
            if (response.status === 200) {
                window.location.href = '/quiz'
            }
        } catch (err) {
            console.error(err)
        }
    }

    return (
        <div className='trainer-body'>
            <nav>
                <UserNav />
            </nav>
            <div className='trainer-container'>
                <img src={wave2} className='admin-wave' />
                <div className="trainer-header">
                    <h1 className="trainer-header-text">Let's learn!</h1>
                </div>
                {concepts[1].loading ? (
                    <div className='loading-container'>
                        <FaSpinner className="loading-icon" />
                    </div>
                ) : (
                    <div className='training-concept' style={{ marginTop: '15vh' }}>
                        <div className="lesson-content">
                            <h3>{concepts[1].title}</h3>
                            <ul>
                                {concepts[1].points.map((point, idx) => (
                                    <li key={idx}>{point}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                )}
                {concepts[2].loading ? (
                    <div className='loading-container'>
                        <FaSpinner className="loading-icon" />
                    </div>
                ) : (
                    <div className='training-concept'>
                        <div className="lesson-content">
                            <h3>{concepts[2].title}</h3>
                            <ul>
                                {concepts[2].points.map((point, idx) => (
                                    <li key={idx}>{point}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                )}
                {concepts[3].loading ? (
                    <div className='loading-container'>
                        <FaSpinner className="loading-icon" />
                    </div>
                ) : (
                    <div className='training-concept'>
                        <div className="lesson-content">
                            <h3>{concepts[3].title}</h3>
                            <ul>
                                {concepts[3].points.map((point, idx) => (
                                    <li key={idx}>{point}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                )}
                <button className='trainer-button' onClick={() => handleTraining(true)}>Complete</button>
            </div>
        </div>
    )
}