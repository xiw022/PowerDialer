import React, { Component } from 'react';
import firebase, { auth, provider } from '../../components/firebase/firebase.js';
import './Account.css';

//js file to handle firebase login functionality
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

//login function changes state to user after successful login
login() {
  auth.signInWithPopup(provider)
    .then((result) => {
      const user = result.user;
      this.setState({
        user
      });
    });
}

//logout function changes state to null after successful logout
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
        {this.state.user ?   //checking what the login state is and changing button
          <button onClick={this.logout}>Log Out</button>
          :
          <button onClick={this.login}>Login</button>
        }
      </div>
      {this.state.user ?   //if you are logged in show the user image below"
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
