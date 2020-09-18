import React from 'react';

import BlackboardBackground from './BlackboardBackground/BlackboardBackground';
import Logo from '../../UI/Logo/Logo';
import classes from './LeftHalf.module.css';

const leftHalf = props => (
    <div className={classes.LeftHalf}>
        <BlackboardBackground />
        <div className={classes.Logo}>
            <Logo />
        </div>
    </div>
)

export default leftHalf;