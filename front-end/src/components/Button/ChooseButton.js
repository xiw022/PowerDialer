import React, { Component } from 'react';
import { Button } from 'react-bootstrap';
import ReactFileReader from 'react-file-reader';

var datad = {};
var firstName = [];
var lastName = [];

class ChooseButton extends Component {

  handleFiles = files => {
      var reader = new FileReader();
      reader.onload = function(e) {
      // Use reader.result
      //alert(reader.result)
      var x = reader.result.split("\n")

      //var y = x.split(",")
      //console.log(y)
      x.map((entry) => {
        var cind = entry.indexOf(",")
        var fname = entry.substring(0,cind)
        var lname = entry.substring(cind+1)
        firstName.push(fname)
        lastName.push(lname)
        datad["fname"] = firstName
        datad["lname"] = lastName
      });
      console.log(datad)
      }

    reader.readAsText(files[0]);
    return firstName;
  }  

  render() {

    return (
      <ReactFileReader handleFiles={this.handleFiles} fileTypes={'.csv'}>
        <button className='btn'>Choose File</button>
      </ReactFileReader>
    );
  }
};

export default ChooseButton;

