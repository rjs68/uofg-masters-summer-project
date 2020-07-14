import React, { Component } from 'react';
import axios from 'axios';

import LoginInput from '../../../components/LoginInput/LoginInput';
import SignUpInput from '../../../components/SignUpInput/SignUpInput';
import classes from './RightHalf.module.css';

class RightHalf extends Component {
    constructor(props) {
        super(props);
        this.state = {
            mode: "login"
        };

        axios.defaults.xsrfCookieName = 'csrftoken'
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

        this.handleModeChange = this.handleModeChange.bind(this);
        this.handleConfirmEmailChange = this.handleConfirmEmailChange.bind(this);
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
        this.handleConfirmPasswordChange = this.handleConfirmPasswordChange.bind(this)
        this.handleEnrolmentKeyChange = this.handleEnrolmentKeyChange.bind(this);
        this.handleFirstNameChange = this.handleFirstNameChange.bind(this);
        this.handleLastNameChange = this.handleLastNameChange.bind(this);
        this.loginHandler = this.loginHandler.bind(this);
        this.signUpHandler = this.signUpHandler.bind(this);
    };

    handleModeChange(){
        const mode = this.state.mode;
        var newMode;
        if(mode === "login"){
            newMode = "sign up";
        }else{
            newMode = "login";
        }
        this.setState({mode: newMode});
    }

    handleConfirmEmailChange(event){
        this.setState({confirmEmail: event.target.value})
    }

    handlePasswordChange(event){
        this.setState({password: event.target.value})
    }

    handleConfirmPasswordChange(event){
        this.setState({confirmPassword: event.target.value})
    }
    
    handleEnrolmentKeyChange(event){
        this.setState({enrolmentKey: event.target.value})
    }
    
    handleFirstNameChange(event){
        this.setState({firstName: event.target.value})
    }
    
    handleLastNameChange(event){
        this.setState({lastName: event.target.value})
    }

    loginHandler() {
        axios.post('/login/', {
            email: this.props.email,
            password: this.state.password
          })
          .then((response) => {
            if(response.data === "Login Successful"){
                this.setState({password: ""});
                this.props.onUserAuthenticated();
            }else{
                console.log(response.data);
            }
          }, (error) => {
            console.log(error);
          });
    }

    signUpHandler() {
        const email = this.props.email
        const password = this.state.password
        if(email!=this.state.confirmEmail || password!=this.state.confirmPassword){
            console.log("Emails or passwords do not match")
        }else{
            axios.post('/signup/', {
                email: email,
                password: password,
                enrolmentKey: this.state.enrolmentKey,
                firstName: this.state.firstName,
                lastName: this.state.lastName
            })
            .then((response) => {
                if(response.data === "User Creation Successful"){
                    this.setState({
                        password: "",
                        confirmPassword: ""
                    });
                    this.props.onUserAuthenticated();
                }else{
                    console.log(response.data);
                }
              }, (error) => {
                console.log(error);
              });
        }
    }

    render(){
        var inputMode;

        if(this.state.mode === "login"){
            inputMode = <LoginInput login={this.loginHandler}
                                    onEmailChange={this.props.onEmailChange}
                                    onPasswordChange={this.handlePasswordChange}
                                    onModeChange={this.handleModeChange}/>
        }else {
            inputMode = <SignUpInput signUp={this.signUpHandler}
                                    onEmailChange={this.props.onEmailChange}
                                    onConfirmEmailChange={this.handleConfirmEmailChange}
                                    onPasswordChange={this.handlePasswordChange}
                                    onConfirmPasswordChange={this.handleConfirmPasswordChange}
                                    onModeChange={this.handleModeChange}
                                    onEnrolmentKeyChange={this.handleEnrolmentKeyChange}
                                    onFirstNameChange={this.handleFirstNameChange}
                                    onLastNameChange={this.handleLastNameChange}/>
        }

        return (
            <div className={classes.RightHalf}>
                {inputMode}
            </div>
        )
    }
}

export default RightHalf;