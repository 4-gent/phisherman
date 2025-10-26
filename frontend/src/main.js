import React from 'react'
import { Link } from 'react-router-dom'
import './styles/main.css'

export default function Main() {
	return (
		<div className="main-container">
			<h1>🎣 Phisherman</h1>
			<p>AI-Powered Phishing Training Platform</p>
			<p>Built for CalHacks 2025 - Fetch.ai Track</p>

			<div className="nav-container">
				<Link to="/login">Login</Link>
				<Link to="/register">Register</Link>
				<Link to="/trainer">Trainer</Link>
				<Link to="/quiz">Quiz</Link>
			</div>

			<div style={{ marginTop: '2rem', fontSize: '1rem', opacity: 0.8 }}>
				<p>🚀 5 AI Agents Ready for Agentverse Registration</p>
				<p>🔒 Safe Phishing Training for Cybersecurity Awareness</p>
			</div>
		</div>
	)
}
