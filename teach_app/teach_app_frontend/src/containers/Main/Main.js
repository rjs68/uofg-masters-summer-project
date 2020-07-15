import React, { Component } from 'react';

import Aux from '../../hoc/Auxiliary/Auxiliary';
import Toolbar from '../../components/Navigation/Toolbar/Toolbar';

class Main extends Component {
    render() {
        return (
            <Aux>
                <Toolbar />
                Content Container
            </Aux>
        )
    }
}

export default Main;