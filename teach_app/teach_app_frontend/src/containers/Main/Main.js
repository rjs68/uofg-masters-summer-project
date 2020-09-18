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
          content: props.cookies.get('page') || "home",
          //dictionary of all the pages and the components to be displayed
          contentPages: {
                "home": <Home email={this.props.email} 
                                userType={this.props.userType} 
                                cookies={this.props.cookies}/>,
                "units": <Units email={this.props.email} 
                                userType={this.props.userType} 
                                cookies={this.props.cookies} />,
                "lectures": <Lectures email={this.props.email} 
                                        userType={this.props.userType} 
                                        cookies={this.props.cookies} />,
                "assignments": <Assignments email={this.props.email} 
                                            userType={this.props.userType}
                                            cookies={this.props.cookies} />,
                "grades": <Grades email={this.props.email} 
                                    userType={this.props.userType} 
                                    cookies={this.props.cookies}/>
          }
        };

        this.navigationHandler = this.navigationHandler.bind(this);
    }

    navigationHandler(page) {
        //sets the new page as a cookie so users are guided back here on reload
        this.props.cookies.set('page', page, { path: '/'});
        this.setState({
            content: page
        });
    }
    
    render() {
        const pageContent = this.state.contentPages[this.state.content];

        //displays toolbar and the selected page
        return (
            <Aux>
                <Toolbar navigation={this.navigationHandler}/>
                {pageContent}
            </Aux>
        )
    }
}

export default Main;