import React, { Component } from 'react';

import Aux from '../../hoc/Auxiliary/Auxiliary';
import LeftHalf from '../LoginScreen/LeftHalf/LeftHalf';
import RightHalf from '../LoginScreen/RightHalf/RightHalf';

class LoginScreen extends Component {
    render() {
        return (
            <Aux>
                <LeftHalf />
                <RightHalf email={this.props.email}
                            onEmailChange={this.props.onEmailChange} 
                            onUserAuthenticated={this.props.onUserAuthenticated} 
                            cookies={this.state.cookies} />
            </Aux>
        )
    }
}

export default LoginScreen;
