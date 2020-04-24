import React, { useState } from 'react';


function Gemeente(props) {

    return (
        <div class="gemeente">
            <p>{props.info[0]}</p>
        </div>
    );
}

export default Gemeente;
