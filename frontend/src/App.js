import React from 'react'
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom'
import Main from './main'
import Login from './routes/login';
import Register from './routes/register';
import Trainer from './routes/trainer';
import Quiz from './routes/quiz';
import Admin from './routes/admin';
import Dashboard from './routes/dashboard';
import Campaign from './routes/campaign';
import Prompt from './routes/prompt';

function App() {
  return (
	<Router>
		<Routes>
			<Route exact path="/" element={<Main />} />
			<Route path="/login" element={<Login />} />
			<Route path="/register" element={<Register />} />
			<Route path="/trainer" element={<Trainer />} />
			<Route path="/quiz" element={<Quiz />} />
			<Route path="/admin" element={<Admin />} />
			<Route path="/dashboard" element={<Dashboard />} />
			<Route path="/campaign" element={<Campaign />} />
			<Route path="/prompt" element={<Prompt />} />
		</Routes>
	</Router>
  );
}

export default App;
