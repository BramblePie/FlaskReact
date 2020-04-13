import React, { useState } from 'react';


function Gemeente(props) {

    const getStyle = () => (
        {
            color: '#ff0000'
        }
    );


    return (
        <div style={getStyle()}>
            <p>{props.info[0]}</p>
        </div>
    );
}

export default Gemeente;
