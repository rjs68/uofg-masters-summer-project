import React from 'react';

import BlackboardBackground from './BlackboardBackground/BlackboardBackground';
import Logo from '../../UI/Logo/Logo';
import classes from './LeftHalf.module.css';

const leftHalf = props => (
    //displays blackboard background and logo on left half of the screen
    <div className={classes.LeftHalf}>
        <BlackboardBackground />
        <div className={classes.Logo}>
            <Logo />
        </div>
    </div>
)

export default leftHalf;