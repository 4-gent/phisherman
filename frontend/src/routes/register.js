import React, { useState } from 'react'
import axios from 'axios'
import '../styles/register.css'
import { ToastContainer, toast } from "react-toastify"
import 'react-toastify/dist/ReactToastify.css'

export default function Register(){
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [email, setEmail] = useState('')
    const [company, setCompany] = useState('')

    const handleRegister = async(e) => {
        e.preventDefault()

        try{
            const response = await axios.post('http://localhost:8080/register', {
                username: username,
                password: password,
                email: email,
                company: company
            }, {withCredentials: true})

            if(response.status === 200){
                toast.success("Rerouting to Login", {autoClose: 1500})
                setTimeout(() => {
                    window.location.href = '/login'
                }, 1500)
            }

        } catch (err) {
            if(err.data === false || err.status === 401 || err.data === null){
                toast.error('Check username and password and try again', {autoClose: 1500})
            }
            else if(err.status === 409){
				toast.error('User already exists, please try again', {autoClose: 1500})
			}
            else
                toast.error('Something happened server side', {autoClose: 1500})
            console.log(err)
        }
    }

    return(
        <div className='register-body'>
            <form onSubmit={handleRegister} className='register-form'>
                <h1>Create an Account</h1>
                <input className='register-input' placeholder='Username' required onChange={(e) => setUsername(e.target.value)} />
                <input className='register-input' type="password" placeholder='Password' required onChange={(e) => setPassword(e.target.value)} />
                <input className='register-input' placeholder='Email' required onChange={(e) => setEmail(e.target.value)} />
                <input className='register-input' placeholder='Company' required onChange={(e) => setCompany(e.target.value)} />
                <button className='register-button' type='submit'>Create Account</button>
            </form>
            <ToastContainer />
        </div>
    )
}
