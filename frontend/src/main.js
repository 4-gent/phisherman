import React from 'react'
import { Link } from 'react-router-dom'
import './styles/main.css'
import Navigation from './components/navbar'
import Logo from './styles/images/Logo.png'

export default function Main() {
	return (
		<div className="main-body">
			<nav>
				<Navigation />
			</nav>
			<div className='main-container'>
				<div className='main-header d-flex flex-row justify-content-around'>
					<div className='d-flex flex-column'>
						<h1 style={{fontSize: '8em'}}>Phisherman</h1>
						<p style={{fontSize: '3em'}}>Your enterprise solution to security awareness</p>
					</div>
					<div className='d-flex flex-column'>
						<img alt='logo-here' />
					</div>
				</div>
			</div>
		</div>
	)
}
