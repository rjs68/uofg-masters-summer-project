import React, { Component } from "react";
import { render } from "react-dom";

import Aux from '../hoc/Auxiliary/Auxiliary';
import LoginScreen from "../containers/LoginScreen/LoginScreen";
import Main from "../containers/Main/Main";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      authenticated: false
    };

    this.handleEmailChange = this.handleEmailChange.bind(this);
    this.handleUserAuthenticated = this.handleUserAuthenticated.bind(this);
  }

  handleEmailChange(event){
    this.setState({email: event.target.value})
  }

  handleUserAuthenticated(userType){
    this.setState({
        authenticated: true,
        userType: userType
    })
  }

  render() {
    var container;

    if(this.state.authenticated){
      container = <Main email={this.state.email} 
                        userType={this.state.userType}/>
    }else {
      container = <LoginScreen email={this.state.email} 
                                password={this.state.password}
                                onEmailChange={this.handleEmailChange}
                                onPasswordChange={this.handlePasswordChange}
                                onUserAuthenticated={this.handleUserAuthenticated}/>
    }

    return (
        <Aux>
           {container} 
        </Aux>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);