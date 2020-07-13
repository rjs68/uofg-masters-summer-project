import React, { Component } from "react";
import { render } from "react-dom";

import Aux from '../hoc/Auxiliary/Auxiliary';
// import LeftHalf from '../containers/LoginScreen/LeftHalf/LeftHalf';
// import RightHalf from '../containers/LoginScreen/RightHalf/RightHalf';
import LoginScreen from "../containers/LoginScreen/LoginScreen";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: "",
      password: ""
    };

    this.handleEmailChange = this.handleEmailChange.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
  }

  handleEmailChange(event){
    this.setState({email: event.target.value})
  }

  handlePasswordChange(event){
    this.setState({password: event.target.value})
  }

//   componentDidMount() {
//     fetch("api/teach_user")
//       .then(response => {
//         if (response.status > 400) {
//           return this.setState(() => {
//             return { placeholder: "Something went wrong!" };
//           });
//         }
//         return response.json();
//       })
//       .then(data => {
//         this.setState(() => {
//           return {
//             data,
//             loaded: true
//           };
//         });
//       });
//   }

  render() {
    return (
        <Aux>
            <LoginScreen email={this.state.email} 
                        password={this.state.password}
                        onEmailChange={this.handleEmailChange}
                        onPasswordChange={this.handlePasswordChange}/>
        </Aux>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);