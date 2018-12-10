import React, { Component } from 'react';
import ReactUploadFile from 'react-upload-file';
import UploadButton from '../../components/Button/UploadButton.js'
import ChooseButton from '../../components/Button/ChooseButton.js'
import ReactFileReader from 'react-file-reader';
import $ from 'jquery';

var test=""
class Uploader extends Component {
  constructor(props) {
    super(props);
    console.log("[Component.js] Inside Constructor", props);
    this.inputElement = React.createRef();
  }
  handleFiles = files => {
    var reader = new FileReader();
    var fd = new FormData();
    reader.onload = function(e) {
    //
      file_result = reader.result  //gets csv data from upload and stores in a variable
      $.ajax({
      type: 'POST',
      url: "http://0.0.0.0:8081/load_newpatient_data",
      //dataType: 'jsonp',
      dataType: 'jsonp',
      contentType: 'application/json; charset=utf-8',
      data: {"file": file_result},
      success: function(data) {
       alert("");
     }.bind(this),
      error: function(error) {
        console.log("error")
      }
    })
    }
    reader.readAsText(files[0])
  }

  render() {
    const options = {
        baseUrl: 'http://127.0.0.1',
        query: {
          warrior: 'fight'
        }
      }

    return (
       <ReactFileReader handleFiles={this.handleFiles} fileTypes={'.csv'}>
        <button className='btn'>File Upload</button>
      </ReactFileReader>
    );
  }
};

export default Uploader;
