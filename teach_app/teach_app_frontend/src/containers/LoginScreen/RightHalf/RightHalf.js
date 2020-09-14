import React, { Component } from 'react';
import axios from 'axios';
import { Alert } from 'react-alert';

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
        this.handleInputChange = this.handleInputChange.bind(this);
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

    handleInputChange(event) {
        this.setState({[event.target.name]: event.target.value});
    }

    loginHandler() {
        axios.post('/login/', {
            email: this.props.email,
            password: this.state.password
          })
          .then((response) => {
            this.setState({password: ""});
            if(response.data === "Teacher Login Successful"){
                this.props.onUserAuthenticated("teacher");
            }else if(response.data === "Student Login Successful"){
                this.props.onUserAuthenticated("student");
            }else{
                alert("Login unsuccesful - please check your email and password and try again")
            }
          }, (error) => {
            alert("Login unsuccesful - please check your email and password and try again")
          });
    }

    signUpHandler() {
        const email = this.props.email
        const password = this.state.password
        if(email!=this.state.confirmEmail){
            alert("Emails do not match")
        }else if(password!=this.state.confirmPassword){
            alert("Passwords do not match")
        }else{
            axios.post('/signup/', {
                email: email,
                password: password,
                enrolmentKey: this.state.enrolmentKey,
                firstName: this.state.firstName,
                lastName: this.state.lastName
            })
            .then((response) => {
                this.setState({
                    password: "",
                    confirmPassword: ""
                });
                if(response.data === "Teacher Creation Successful"){
                    this.props.onUserAuthenticated("teacher");
                }else if(response.data === "Student Creation Successful"){
                    this.props.onUserAuthenticated("student");
                }else{
                    alert("Sign up unsuccesful - please check your enrolment key and try again")
                }
              }, (error) => {
                alert("Sign up unsuccesful - please check your enrolment key and try again")
              });
        }
    }

    render(){
        var inputMode;

        if(this.state.mode === "login"){
            inputMode = <LoginInput login={this.loginHandler}
                                    onEmailChange={this.props.onEmailChange}
                                    onInputChange={this.handleInputChange}
                                    onModeChange={this.handleModeChange}/>
        }else {
            inputMode = <SignUpInput signUp={this.signUpHandler} 
                                    onInputChange={this.handleInputChange}
                                    onEmailChange={this.props.onEmailChange} 
                                    onModeChange={this.handleModeChange} />
        }

        return (
            <div className={classes.RightHalf}>
                {inputMode}
            </div>
        )
    }
}

export default RightHalf;