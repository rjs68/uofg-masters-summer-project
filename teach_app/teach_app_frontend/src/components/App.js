import React, { Component } from 'react';
import { render } from 'react-dom';
import Cookies from 'universal-cookie';

import Aux from '../hoc/Auxiliary/Auxiliary';
import LoginScreen from "../containers/LoginScreen/LoginScreen";
import Main from "../containers/Main/Main";

//Entrypoint container for application

class App extends Component {
  constructor(props) {
    super(props);

    const cookies = new Cookies();

    this.state = {
      cookies: cookies,
      //attempt to retrieve previously logged in user from cookies
      email: cookies.get('userEmail'),
      userType: cookies.get('userType'),
      authenticated: cookies.get('authenticated') || false
    };

    this.handleEmailChange = this.handleEmailChange.bind(this);
    this.handleUserAuthenticated = this.handleUserAuthenticated.bind(this);
  }

  handleEmailChange(event){
    this.setState({
      email: event.target.value
    });
  }

  handleUserAuthenticated(userType){
    //set cookies to keep user logged in
    this.state.cookies.set('userEmail', this.state.email, { path: '/'});
    this.state.cookies.set('userType', userType, { path: '/' });
    this.state.cookies.set('authenticated', true, { path: '/', maxAge: 3600 });
    this.setState({
        authenticated: true,
        userType: userType
    })
  }

  render() {
    var container;

    if(this.state.authenticated){
      container = <Main email={this.state.email} 
                        userType={this.state.userType}
                        cookies={this.state.cookies} />
    }else {
      container = <LoginScreen email={this.state.email} 
                                password={this.state.password}
                                onEmailChange={this.handleEmailChange}
                                onPasswordChange={this.handlePasswordChange}
                                onUserAuthenticated={this.handleUserAuthenticated}
                                cookies={this.state.cookies}/>
    }

    return (
        <Aux>
           {container} 
        </Aux>
    );
  }
}

export default App;

//select element in index.html to contain the application
const container = document.getElementById("app");
render(<App />, container);