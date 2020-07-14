import React from 'react';

// import classes from './LoginInput.module.css';
import Button from '../UI/Button/Button';

const signUpInput = props => (
    <div>
        <Button>Teacher</Button>
        <Button>Student</Button>
        <input onChange={props.onEnrolmentCodeChange}
                type="text"
                name="enrolment code"
                placeholder="Enrolment Code" />
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
        <input type="text" 
                name="confirm email" 
                placeholder="Confirm Email" />
        <input onChange={props.onPasswordChange}
                type="password" 
                name="password" 
                placeholder="Password" />
        <input type="password" 
                name="confirm password" 
                placeholder="Confirm Password" />
        <Button clicked={props.login}>Sign Up</Button>
        <p>Already have an account?</p>
        <Button clicked={props.onModeChange}>Login</Button>
    </div>
)

export default signUpInput;