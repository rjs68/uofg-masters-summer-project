import React from 'react';

import teachLogo from '../../../../static/frontend/teach_logo_white.png';
import classes from './Logo.module.css';

const logo = props => (
    <div className={classes.Logo} onClick={() => props.navigation("home")}>
        <img src={teachLogo} alt="Teach Logo" />
    </div>
)

export default logo;