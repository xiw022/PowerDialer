import React, { Component } from 'react';
import logo from './logo.png';
//import Table from './containers/Table/Table.js'
import Uploader from './containers/Uploader/Uploader.js'
import Account from './containers/Account/Account.js'
import './App.css';
import Table from './containers/Table/Table.js'

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo"/>
          <h1 className="App-title">Power Dialer</h1>
          <Account/>
        </header>
        <p className="App-intro">
          <Uploader/>
          <Table/>
        </p>
      </div>
    );
  }
};


export default App;
