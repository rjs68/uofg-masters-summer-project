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

        this.handleModeChange = this.handleModeChange.bind(this);
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
        this.handleEnrolmentCodeChange = this.handleEnrolmentCodeChange.bind(this);
        this.handleFirstNameChange = this.handleFirstNameChange.bind(this);
        this.handleLastNameChange = this.handleLastNameChange.bind(this);
        this.loginHandler = this.loginHandler.bind(this);
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

    handlePasswordChange(event){
        this.setState({password: event.target.value})
    }
    
    handleEnrolmentCodeChange(event){
        this.setState({enrolmentCode: event.target.value})
    }
    
    handleFirstNameChange(event){
        this.setState({firstName: event.target.value})
    }
    
    handleLastNameChange(event){
        this.setState({lastName: event.target.value})
    }

    loginHandler() {
        axios.defaults.xsrfCookieName = 'csrftoken'
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

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

    render(){
        var inputMode;

        if(this.state.mode === "login"){
            inputMode = <LoginInput login={this.loginHandler}
                                    onEmailChange={this.props.onEmailChange}
                                    onPasswordChange={this.handlePasswordChange}
                                    onModeChange={this.handleModeChange}/>
        }else {
            inputMode = <SignUpInput onEmailChange={this.props.onEmailChange}
                                    onPasswordChange={this.handlePasswordChange}
                                    onModeChange={this.handleModeChange}
                                    onEnrolmentCodeChange={this.handleEnrolmentCodeChange}
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