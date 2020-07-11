import React, { Component } from 'react';

import Layout from './hoc/Layout/Layout';
import LoginScreen from './containers/LoginScreen/LoginScreen';

class App extends Component {
  render() {
    return (
      <Layout>
        <LoginScreen />
      </Layout>
    );
  }
}

export default App;
