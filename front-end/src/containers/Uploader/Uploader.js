import React, { Component } from 'react';
import ReactUploadFile from 'react-upload-file';
import UploadButton from '../../components/Button/UploadButton.js'
import ChooseButton from '../../components/Button/ChooseButton.js'


class Uploader extends Component {
  constructor(props) {
    super(props);
    console.log("[Component.js] Inside Constructor", props);
    this.inputElement = React.createRef();
  }
  render() {
    const options = {
        baseUrl: 'http://127.0.0.1',
        query: {
          warrior: 'fight'
        }
      }

    return (
       <ReactUploadFile options={options}  chooseFileButton={<ChooseButton />} uploadFileButton={<UploadButton />} />
    );
  }
};

export default Uploader;
