import React from 'react';

import classes from './SignUpInput.module.css';
import Button from '../UI/Button/Button';

const signUpInput = props => (
    <div className={classes.SignUpInput}>
        <input onChange={props.onEnrolmentKeyChange}
                type="text"
                name="enrolment key"
                placeholder="Enrolment Key" />
        <input onChange={props.onFirstNameChange}
                type="text"
                name="first name"
                placeholder="First Name" />
        <input onChange={props.onLastNameChange}
                type="text"
                name="last name"
                placeholder="Last Name" />
        <input onChange={props.onEmailChange}
                type="text" 
                name="email" 
                placeholder="Email" />
        <input onChange={props.onConfirmEmailChange}
                type="text" 
                name="confirm email" 
                placeholder="Confirm Email" />
        <input onChange={props.onPasswordChange}
                type="password" 
                name="password" 
                placeholder="Password" />
        <input onChange={props.onConfirmPasswordChange}
                type="password" 
                name="confirm password" 
                placeholder="Confirm Password" />
        <Button clicked={props.signUp}>Sign Up</Button>
        <p>Already have an account?</p>
        <Button clicked={props.onModeChange}>Login</Button>
    </div>
)

export default signUpInput;