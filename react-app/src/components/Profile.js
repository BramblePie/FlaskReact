import React, { useState, useEffect } from 'react';
import './Profile.css'


function Profile(props) {

    const [aant_inw, setAant_inw] = useState(500000);

    useEffect(() => {
        props.getGemeentes(aant_inw);
    }, [aant_inw]);

    return (
        <div class="profile">
            <h2>Profiel</h2>
            <input type="number" min="0" step="1000"
                value={aant_inw} onChange={(e) => setAant_inw(e.target.value)} />
        </div>
    );
}

export default Profile;
