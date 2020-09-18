import React from 'react';

import classes from './LoginInput.module.css';
import Button from '../../../UI/Button/Button';

const loginInput = props => (
    <div className={classes.LoginInput}>
        <input onChange={props.onEmailChange}
                type="text" 
                name="email" 
                placeholder="Email" />
        <input onChange={props.onInputChange}
                type="password" 
                name="password" 
                placeholder="Password" />
        <Button clicked={props.login}>Login</Button>
        <p>Don't have an account?</p>
        <Button clicked={props.onModeChange}>Sign Up</Button>
    </div>
)

export default loginInput;