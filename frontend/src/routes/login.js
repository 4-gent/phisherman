import React, { useState } from 'react'
import axios from 'axios'
import '../styles/login.css'
import { ToastContainer, toast } from "react-toastify"
import 'react-toastify/dist/ReactToastify.css'

import wave from '../styles/images/support_images/wave.svg'
import Navigation from '../components/navbar'

export default function Login(){
	const [username, setUsername] = useState('')
	const [password, setPassword] = useState('')

	const handleLogin = async(e) => {
		e.preventDefault()

		try{
			const response = await axios.post('http://localhost:8080/login', {
				username: username,
				password: password
			}, {withCredentials: true})

			if(response.status === 200){
				toast.success("Rerouting to Dashboard", {autoClose: 1500})
				setTimeout(() => {
					window.location.href = '/dashboard'
				}, 1500)
			}
			else if(response.status === 201){
				toast.success("Rerouting to Admin Dashboard", {autoClose: 1500})
				setTimeout(() => {
					window.location.href = '/admin'
				}, 1500)
			}

		} catch (err) {
			if(err.data === false || err.status === 401 || err.data === null){
                toast.error('Check username and password and try again', {autoClose: 1500})
            }
			else if(err.status === 401){
				toast.error('Wrong username or password please try again', {autoClose: 1500})
			}
            else
                toast.error('Something happened server side', {autoClose: 1500})
            console.log(err)
		}
	}

	return(
		<div className='login-body'>
			<img src={wave} className='login-wave'/>
			<nav>
				<Navigation />
			</nav>
			<form onSubmit={handleLogin} className='login-form d-flex flex-column align-items-center'>
				<h1>Login</h1>
				<input className='login-input' placeholder='Username' required onChange={(e) => setUsername(e.target.value)} />
				<input className='login-input' type="password" placeholder='Password' required onChange={(e) => setPassword(e.target.value)} />
				<button className='login-button' type='submit'>Login</button>
			</form>
			<ToastContainer />
		</div>
	)
}
