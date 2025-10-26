import React, {useState, useEffect} from "react";
import '../styles/dashboard.css'
import axios from "axios";

import wave2 from '../styles/images/support_images/wave2.svg'
import UserNav from "../components/usernavbar";

export default function Dashboard(){
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
        <div className='dashboard-body'>
            <nav>
                <UserNav />
            </nav>
            <div className="dashboard-container">
                <img src={wave2} className="dashboard-wave"/>
                <div className="dashboard-header">
                    <h1 className="dashboard-header-text">Welcome to your dashboard, {username}</h1>
                </div>
                <div className="dashboard-upper">
                    <div className="dashboard-trainings">

                    </div>
                    <div className="dashboard-personal-score">

                    </div>
                </div>
                <div className="dashboard-lower">
                    <div className="dashboard-leaderboard">
                        
                    </div>
                </div>
            </div>
        </div>
    )
}