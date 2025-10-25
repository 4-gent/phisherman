import React, {useState} from 'react'
import axios from 'axios'
import DashNav from '../components/dashnavbar'
import '../styles/admin.css'

export default function Admin(){
    const handleEmail = async(e) => {
        try{
            const response = await axios.post("http://localhost:8080/api/email", {withCredentials: true})
            console.log(response)
        } catch (err){
            console.log(err)
        }
    }
    
    return(
        <div className='admin-body'>
            <nav>
                <DashNav />
            </nav>
            <form onSubmit={handleEmail}>
                <button type='submit'>Send Email Test</button>
            </form>
        </div>
    )
}