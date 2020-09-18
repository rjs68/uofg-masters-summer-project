import React, { Component } from 'react';

import Aux from '../../hoc/Auxiliary/Auxiliary';
import LeftHalf from '../../components/LoginScreen/LeftHalf/LeftHalf';
import RightHalf from '../../components/LoginScreen/RightHalf/RightHalf';

class LoginScreen extends Component {
    render() {
        return (
            <Aux>
                <LeftHalf />
                <RightHalf email={this.props.email}
                            onEmailChange={this.props.onEmailChange} 
                            onUserAuthenticated={this.props.onUserAuthenticated} 
                            cookies={this.props.cookies} />
            </Aux>
        )
    }
}

export default LoginScreen;
