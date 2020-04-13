import React, { useState, useEffect } from 'react';

import Clock from './components/Clock';

function App() {

	const [count, setCount] = useState(0);
	const [num, setNum] = useState(0);

	const [gemeentes, setGemeentes] = useState();
	const [inwCount, setInwCount] = useState(500000);

	useEffect(() => {
		// Haal data uit Flask API
		fetch(`http://127.0.0.1/api/number/${count}`)
			.then((response) => {
				return response.json();
			}).then((data) => {
				console.log(data);
				console.log(data[count]);
				setNum(data[count]);
			});

	}, [count]);

	useEffect(() => {
		// Haal gemeentes op uit Flask API
		fetch(`http://127.0.0.1/api/gemeente/${inwCount}`)
			.then((response) => {
				return response.json();
			}).then((data) => {
				setGemeentes(Object.entries(data));
				console.log(gemeentes);
			});
	}, [inwCount])

	const getStyle = () => (
		{
			color: num % 2 == 0 ? '#800080' : '#FFFFFF'
		}
	);

	return (
		<div >
			<Clock />
			<input type="number" min="0" step="1000" value={inwCount} onChange={(e) => setInwCount(e.target.value)} />
			<div>
				<button onClick={() => setCount(count + 1)}>
					Clicked {count} times
      			</button>
				<p style={getStyle()}>
					{num}
				</p>
			</div>
		</div>
	);
}

export default App;
