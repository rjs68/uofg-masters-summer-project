import React from 'react';

import BlackboardBackground from '../../../components/BlackboardBackground/BlackboardBackground';
import Logo from '../../../components/Logo/Logo';
import classes from './LeftHalf.module.css';

const leftHalf = props => (
    <div className={classes.LeftHalf}>
        <BlackboardBackground />
        <Logo />
    </div>
)

export default leftHalf;