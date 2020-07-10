import React from 'react';

import classes from './LoginInput.module.css';

const loginInput = props => (
    <div className={classes.LoginInput}>
        <input type="text" name="email" placeholder="Email" />
        <input type="password" name="password" placeholder="Password" />
        <button>Login</button>
    </div>
)

export default loginInput;