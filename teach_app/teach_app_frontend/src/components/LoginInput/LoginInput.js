import React from 'react';

import classes from './LoginInput.module.css';
import Button from '../UI/Button/Button';

const loginInput = props => (
    <div className={classes.LoginInput}>
        <input type="text" name="email" placeholder="Email" />
        <input type="password" name="password" placeholder="Password" />
        <Button>Login</Button>
    </div>
)

export default loginInput;