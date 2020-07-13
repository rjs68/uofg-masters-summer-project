import React from 'react';

import classes from './LoginInput.module.css';
import Button from '../UI/Button/Button';

const loginInput = props => (
    <div className={classes.LoginInput}>
        <input onChange={props.onEmailChange}
                type="text" 
                name="email" 
                placeholder="Email" />
        <input onChange={props.onPasswordChange}
                type="password" 
                name="password" 
                placeholder="Password" />
        <Button clicked={props.login}>Login</Button>
    </div>
)

export default loginInput;