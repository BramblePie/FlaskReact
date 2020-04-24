import React, { useState, useEffect } from 'react';
import './Profile.css'


function Profile(props) {

    const [inwCount, setInwCount] = useState(500000);

    useEffect(() => {
        props.getGemeentes(inwCount);
    }, [inwCount])

    return (
        <div class="profile">
            <h2>Profiel</h2>
            <input type="number" min="0" step="1000"
                value={inwCount} onChange={(e) => setInwCount(e.target.value)} />
        </div>
    );
}

export default Profile;
