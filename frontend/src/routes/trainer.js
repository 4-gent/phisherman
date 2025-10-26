import React, {useState, useEffect, use} from 'react'
import '../styles/trainer.css'
import '../styles/loading.css'
import { io } from "socket.io-client";
import {FaSpinner} from "react-icons/fa"
import axios from 'axios';

import wave2 from '../styles/images/support_images/wave2.svg'
import UserNav from '../components/usernavbar';

export default function Trainer(){
    const [oneLoading, setOneLoading] = useState(true)
    const [twoLoading, setTwoLoading] = useState(true)
    const [threeLoading, setThreeLoading] = useState(true)

    const [oneText, setOneText] = useState('')
    const [twoText, setTwoText] = useState('')
    const [threeText, setThreeText] = useState('')

    useEffect(() => {
        const socket = io('http://localhost:8080', {withCredentials: true})

        socket.on('connect', () => console.log('socket connected', socket.id))

        socket.emit('join_training', {room: 'personal'})

        socket.on('concept_update', (msg) => {
            console.log('concept_update', msg)
            const {concept, status, text } = msg || {}

            if(concept === 1){
                if (text) setOneText(text)
                if (status === 'done') setOneLoading(false)
            }
            if(concept === 2){
                if (text) setTwoText(text)
                if (status === 'done') setTwoLoading(false)
            }
            if(concept === 3){
                if (text) setThreeText(text)
                if (status === 'done') setThreeLoading(false)
            }
        })

        return () => {
            socket.disconnect()
        }
    }, [])

    const handleTraining = async(training) => {
        try{
            const response = await axios.post('http://localhost:8080/api/completion', {training}, {withCredentials: true})
            if(response.status === 200)
                console.log("training completed")
                window.location.href = '/quiz'
        } catch (err) {
            console.log(err)
        }
    }

    return(
        <div className='trainer-body'>
            <nav>
                <UserNav />
            </nav>
            <div className='trainer-container'>
                <img src={wave2} className='admin-wave' />
                <div className="trainer-header">
                    <h1 className="trainer-header-text">Let's learn!</h1>
                </div>
                {oneLoading ? (
                    <div className='loading-container'>
                        <FaSpinner className="loading-icon" />
                    </div>
                ) : (
                    <div className='training-concept'>
                        <pre>{oneText}</pre>
                    </div>
                )}
                {twoLoading ? (
                    <div className='loading-container'>
                        <FaSpinner className="loading-icon" />
                    </div>
                ) : (
                    <div className='training-concept'>
                        <pre>{twoText}</pre>
                    </div>
                )}
                {threeLoading ? (
                    <div className='loading-container'>
                        <FaSpinner className="loading-icon" />
                    </div>
                ) : (
                    <div className='training-concept'>
                        <pre>{threeText}</pre>
                    </div>
                )}
                <button className='trainer-button' onClick={() => handleTraining(true)}>Complete</button>
            </div>
        </div>
    )
}