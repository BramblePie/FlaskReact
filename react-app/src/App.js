import React, { useState, useEffect } from 'react';

import Gemeente from './components/Gemeente';

function App() {

	const [gemeentes, setGemeentes] = useState([]);
	const [inwCount, setInwCount] = useState(500000);

	useEffect(() => {
		// Haal gemeentes op uit Flask API
		fetch(`http://127.0.0.1/api/gemeente/${inwCount}`)
			.then((response) => {
				return response.json();
			}).then((data) => {
				setGemeentes(Object.entries(data));
			});

	}, [inwCount])

	return (
		<div >
			<input type="number" min="0" step="1000" value={inwCount} onChange={(e) => setInwCount(e.target.value)} />
			<div>
				{gemeentes.map((gemeente) => (
					<Gemeente info={gemeente} />
				))}
			</div>
		</div>
	);
}

export default App;
