import React, { Component } from 'react';

import Aux from '../../hoc/Auxiliary/Auxiliary';
import Toolbar from '../../components/Navigation/Toolbar/Toolbar';
import Home from './Home/Home';
import Units from './Units/Units';
import Assignments from './Assignments/Assignments';
import Grades from './Grades/Grades';

class Main extends Component {
    constructor(props) {
        super(props);
        this.state = {
          content: "home"
        };

        this.navigationHandler = this.navigationHandler.bind(this);
    }

    navigationHandler(page) {
        this.setState({content: page});
    }
    
    render() {
        var pageContent;

        switch(this.state.content){
            case "home":
                pageContent = <Home />;
                break;
            case "units":
                pageContent = <Units email={this.props.email} 
                                        userType={this.props.userType} />;
                break;
            case "assignments":
                pageContent = <Assignments />;
                break;
            case "grades":
                pageContent = <Grades />;
                break;
            default:
                pageContent = <Home />;
        };

        return (
            <Aux>
                <Toolbar navigation={this.navigationHandler}/>
                {pageContent}
            </Aux>
        )
    }
}

export default Main;