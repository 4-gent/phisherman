import React, {useState, useEffect, use} from 'react'
import '../styles/trainer.css'
import '../styles/loading.css'
import { io } from "socket.io-client";
import {FaSpinner} from "react-icons/fa"

export default function Trainer(){
    const [oneLoading, setOneLoading] = useState(true)
    const [twoLoading, setTwoLoading] = useState(true)
    const [threeLoading, setThreeLoading] = useState(true)

    useEffect(() => {
        const socket = io('http://localhost:8080', {withCredentials: true, transports: ['websocket']})

        socket.on('connect', () => console.log('socket connected', socket.id))

        socket.emit('join_training', {room: 'personal'})

        // socket.on('concept_update', (msg) => {
        //     console.log('concept_update', msg)
        //     const {concept, status } = msg || {}
        //     if
        // })
    }, [])

    return(
        <div className='trainer-body'>
            <div className='trainer-container'>
                {oneLoading ? (
                    <div className='loading-container'>
                        <FaSpinner className="loading-icon" />
                    </div>
                ) : (
                    <div className='training-concept-one'>
                    </div>
                )}
                {twoLoading ? (
                    <div className='loading-container'>
                        <FaSpinner className="loading-icon" />
                    </div>
                ) : (
                    <div className='training-concept-two'>
                    </div>
                )}
                {threeLoading ? (
                    <div className='loading-container'>
                        <FaSpinner className="loading-icon" />
                    </div>
                ) : (
                    <div className='training-concept-three'>
                    </div>
                )}
                <button>Complete</button>
            </div>
        </div>
    )
}