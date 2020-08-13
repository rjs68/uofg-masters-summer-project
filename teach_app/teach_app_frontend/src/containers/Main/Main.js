import React, { Component } from 'react';

import Aux from '../../hoc/Auxiliary/Auxiliary';
import Toolbar from '../../components/Navigation/Toolbar/Toolbar';
import Home from './Home/Home';
import Units from './Units/Units';
import Lectures from './Lectures/Lectures';
import Assignments from './Assignments/Assignments';
import Grades from './Grades/Grades';

class Main extends Component {
    constructor(props) {
        super(props);
        this.state = {
          content: "home",
          contentPages: {
                "home": <Home />,
                "units": <Units email={this.props.email} 
                                userType={this.props.userType} />,
                "lectures": <Lectures email={this.props.email} 
                                        userType={this.props.userType} />,
                "assignments": <Assignments email={this.props.email} 
                                            userType={this.props.userType}/>,
                "grades": <Grades />
          }
        };

        this.navigationHandler = this.navigationHandler.bind(this);
    }

    navigationHandler(page) {
        this.setState({content: page});
    }
    
    render() {
        const pageContent = this.state.contentPages[this.state.content];

        return (
            <Aux>
                <Toolbar navigation={this.navigationHandler}/>
                {pageContent}
            </Aux>
        )
    }
}

export default Main;