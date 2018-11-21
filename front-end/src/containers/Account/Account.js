import React, { Component } from 'react';
import firebase, { auth, provider } from '../../components/firebase/firebase.js';
import './Account.css';

class Account extends Component {
  constructor() {
    super();
    this.state = {
      currentItem: '',
      username: '',
      items: [],
      user: null // <-- add this line
    }
    this.login = this.login.bind(this); // <-- add this line
    this.logout = this.logout.bind(this);
}

handleChange(e) {
  /* ... */
}

login() {
  auth.signInWithPopup(provider)
    .then((result) => {
      const user = result.user;
      this.setState({
        user
      });
    });
}

logout() {
  auth.signOut()
    .then(() => {
      this.setState({
        user: null
      });
    });
}

componentDidMount() {
  auth.onAuthStateChanged((user) => {
    if (user) {
      this.setState({ user });
    }
  });
}

render() {
  return (
    <div className="logcol">
      <div className="wrapper">
        {this.state.user ?
          <button onClick={this.logout}>Log Out</button>
          :
          <button onClick={this.login}>Login</button>
        }
      </div>
      {this.state.user ?
      <div>
        <div className='user-profile'>
          <img src={this.state.user.photoURL} className="profile" alt="user_image"/>
        </div>
      </div>
      :
      <div className='wrapper1'>
        <p>Please log in first to see the patients list</p>
      </div>
  }
  </div>
  );
}

};

export default Account;
