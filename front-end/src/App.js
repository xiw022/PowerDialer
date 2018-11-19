import React, { Component } from 'react';
import logo from './logo.svg';
//import Table from './containers/Table/Table.js'
import Uploader from './containers/Uploader/Uploader.js'
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    var ui = new firebaseui.auth.AuthUI(firebase.auth());
      // The start method will wait until the DOM is loaded.
      ui.start('#firebaseui-auth-container', uiConfig);
  }
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Power Dialer</h1>
        </header>
        <p className="App-intro">
          <Uploader/>
        </p>
      </div>
    );
  }
}

export default App;
