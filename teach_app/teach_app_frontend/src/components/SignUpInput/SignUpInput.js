import React from 'react';

import classes from './SignUpInput.module.css';
import Button from '../UI/Button/Button';

const signUpInput = props => (
    <div className={classes.SignUpInput}>
        <input onChange={props.onInputChange}
                type="text"
                name="enrolmentKey"
                placeholder="Enrolment Key" />
        <input onChange={props.onInputChange}
                type="text"
                name="firstName"
                placeholder="First Name" />
        <input onChange={props.onInputChange}
                type="text"
                name="lastName"
                placeholder="Last Name" />
        <input onChange={props.onEmailChange}
                type="text" 
                name="email" 
                placeholder="Email" />
        <input onChange={props.onInputChange}
                type="text" 
                name="confirmEmail" 
                placeholder="Confirm Email" />
        <input onChange={props.onInputChange}
                type="password" 
                name="password" 
                placeholder="Password" />
        <input onChange={props.onInputChange}
                type="password" 
                name="confirmPassword" 
                placeholder="Confirm Password" />
        <Button clicked={props.signUp}>Sign Up</Button>
        <p>Already have an account?</p>
        <Button clicked={props.onModeChange}>Login</Button>
    </div>
)

export default signUpInput;