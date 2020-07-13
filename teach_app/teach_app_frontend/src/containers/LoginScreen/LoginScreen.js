import React, { Component } from 'react';
import Cookies from 'js-cookie';
import axios from 'axios';

import Aux from '../../hoc/Auxiliary/Auxiliary';
import LeftHalf from '../LoginScreen/LeftHalf/LeftHalf';
import RightHalf from '../LoginScreen/RightHalf/RightHalf';

class LoginScreen extends Component {
    loginHandler (email,password) {
        // const csrftoken = Cookies.get('csrftoken');
        // const requestOptions = {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json',
        //                 'X-CSRFToken': csrftoken },
        //     email: email,
        //     password: password
        //     // body: { 'email': email, 'password': password }
        // };
        // fetch("login/", requestOptions)
        axios.defaults.xsrfCookieName = 'csrftoken'
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

        axios.post('/login/', {
            email: email,
            password: password
          });
        // axios({
        //     method: 'post',
        //     url: '/login/',
        //     data: {
        //         'email': email,
        //         'password': password
        //     }
        // });
    }

    render() {
        return (
            <Aux>
                <LeftHalf />
                <RightHalf login={() => this.loginHandler(this.props.email,this.props.password)}
                            onEmailChange={this.props.onEmailChange}
                            onPasswordChange={this.props.onPasswordChange}/>
            </Aux>
        )
    }
}

export default LoginScreen;
