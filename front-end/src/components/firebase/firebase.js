import firebase from 'firebase'
const config = {
 apiKey: "AIzaSyDeJHqjl4vtKoqg7GId7Xxn7huL170nSVk",
 authDomain: "powerdialer-d1bea.firebaseapp.com",
 databaseURL: "https://powerdialer-d1bea.firebaseio.com",
 projectId: "powerdialer-d1bea",
 storageBucket: "powerdialer-d1bea.appspot.com",
 messagingSenderId: "303256369952"
};
firebase.initializeApp(config);
export const provider = new firebase.auth.GoogleAuthProvider();
export const auth = firebase.auth();
export default firebase;
