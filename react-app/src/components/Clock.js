import React, { useState } from 'react';


function Clock() {
    const [date, setDate] = useState(new Date());

    setInterval(() => setDate(new Date()), 1000);


    const makePurple = () => (
        {
            color: '#800080'
        });

    return (
        <div style={makePurple()}>
            <h2>{date.toLocaleTimeString()}</h2>
        </div>
    );
}

export default Clock;
