import React from 'react';

import teachLogo from '../../assets/images/teach_logo_white.png';
import classes from './Logo.module.css';

const logo = props => (
    <div className={classes.Logo}>
        <img src={teachLogo} alt="Teach Logo" />
    </div>
)

export default logo;