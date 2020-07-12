import React, { Component } from 'react';
import { render } from "react-dom";

import Aux from '../../hoc/Auxiliary/Auxiliary';
import LeftHalf from '../LoginScreen/LeftHalf/LeftHalf';
import RightHalf from '../LoginScreen/RightHalf/RightHalf';

class LoginScreen extends Component {
    render() {
        return (
            <Aux>
                <LeftHalf />
                <RightHalf />
            </Aux>
        )
    }
}

export default LoginScreen;

const container = document.getElementById("login");
render(<LoginScreen />, container);