import React, { useState, useEffect } from 'react';
import './App.css'

import Gemeente from './components/Gemeente';
import Profile from './components/Profile';

function App() {

	const [gemeentes, setGemeentes] = useState([]);


	const getGemeentes = (aant_inw) => {
		// Haal gemeentes op uit Flask API
		fetch(`http://127.0.0.1/api/gemeente/${aant_inw}`)
			.then((response) => {
				return response.json();
			}).then((data) => {
				setGemeentes(Object.entries(data));
			});
	};

	return (
		<div class="app">
			<Profile getGemeentes={getGemeentes} />
			<div>
				{gemeentes.map((gemeente) => (
					<Gemeente info={gemeente} />
				))}
			</div>
		</div>
	);
}

export default App;
