import React from 'react';

import LoginInput from '../../../components/LoginInput/LoginInput';
import classes from './RightHalf.module.css';

const rightHalf = props => (
    <div className={classes.RightHalf}>
        <LoginInput />
    </div>
)

export default rightHalf;