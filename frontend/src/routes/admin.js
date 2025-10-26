import React, {useState, useEffect} from 'react'
import axios from 'axios'
import DashNav from '../components/dashnavbar'
import '../styles/admin.css'

import wave from '../styles/images/support_images/wave.svg'

export default function Admin(){
    const handleEmail = async(e) => {
        try{
            const response = await axios.post("http://localhost:8080/api/email", {withCredentials: true})
            console.log(response)
        } catch (err){
            console.log(err)
        }
    }
    
    const [username, setUsername] = useState('')

    useEffect(() => {
        axios.get('http://localhost:8080/api/user', {withCredentials: true})
            .then((response) => {
                setUsername(response.data.username)
            })
            .catch((error) => {
                console.error('Error message: ', error.message)
            })
    })

    return(
        <div className='admin-body'>
            <nav>
                <DashNav />
            </nav>
            <div className="admin-container">
                <img src={wave} className="admin-wave"/>
                <div className="admin-header">
                    <h1 className="admin-header-text">Welcome to your dashboard, {username}</h1>
                </div>
                <div className="admin-upper">
                    <div className="admin-trainings">

                    </div>
                    <div className="admin-personal-score">

                    </div>
                </div>
                <div className="admin-lower">
                    <div className="admin-leaderboard">
                        
                    </div>
                </div>
            </div>
        </div>
    )
}