import React, { Component } from 'react';

import Aux from '../../hoc/Auxiliary/Auxiliary';
import BlackboardBackground from './BlackboardBackground/BlackboardBackground';
import Logo from '../../components/Logo/Logo';

class LoginScreen extends Component {
    render() {
        return (
            <Aux>
                <BlackboardBackground />
                <Logo />
            </Aux>
        )
    }
}

export default LoginScreen;