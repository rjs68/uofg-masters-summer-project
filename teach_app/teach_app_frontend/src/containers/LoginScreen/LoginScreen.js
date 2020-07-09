import React, { Component } from 'react';

import Aux from '../../hoc/Auxiliary/Auxiliary';
import LeftHalf from '../LoginScreen/LeftHalf/LeftHalf';

class LoginScreen extends Component {
    render() {
        return (
            <Aux>
                <LeftHalf />
            </Aux>
        )
    }
}

export default LoginScreen;