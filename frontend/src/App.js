import React from 'react'
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom'
import Main from './main'
import Login from './routes/login';
import Register from './routes/register';
import Trainer from './routes/trainer';
import Quiz from './routes/quiz';

function App() {
  return (
	<Router>
		<Routes>
			<Route exact path="/" element={<Main />} />
			<Route path="/login" element={<Login />} />
			<Route path="/register" element={<Register />} />
			<Route path="/trainer" element={<Trainer />} />
			<Route path="/quiz" element={<Quiz />} />
		</Routes>
	</Router>
  );
}

export default App;
