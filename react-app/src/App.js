import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

import TestBlock from './components/TestBlock';
import Clock from './components/Clock';

function App() {

	const [count, setCount] = useState(0);
	const [num, setNum] = useState(0);

	useEffect(() => {
		// Haal data uit Flask API
		let res = fetch(`http://127.0.0.1/api/number/${count}`)
			.then((response) => {
				return response.json();
			}).then((data) => {
				console.log(data);
				console.log(data[count]);
				setNum(data[count]);
			});

	}, [count]);

	const getStyle = () => ({ color: num % 2 == 0 ? '#800080' : '#FFFFFF' });

	return (
		<div className="App">
			<header className="App-header">
				<Clock />
				<img src={logo} className="App-logo" alt="logo" />
				<p>
					Edit <code>src/App.js</code> and save to reload.
        		</p>
				<button onClick={() => setCount(count + 1)}>
					Clicked {count} times
      			</button>
				<p style={getStyle()}>
					{num}
				</p>
				<TestBlock />
			</header>
		</div>
	);
}

export default App;
