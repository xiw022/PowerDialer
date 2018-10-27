import React, { Component } from 'react';
import logo from './logo.svg';
import Table from './containers/Table/Table.js'
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Power Dialer</h1>
        </header>
        <p className="App-intro">
          <Table/>
        </p>
      </div>
    );
  }
}

export default App;
