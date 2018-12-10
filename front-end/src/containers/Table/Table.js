import React, { Component } from 'react';
import ReactTable from 'react-table'
import 'react-table/react-table.css'
import $ from 'jquery';
import Popup from 'react-popup';
import ReactDOM from 'react-dom';
import './Table.css';
//import {firstName} from '../../components/Button/ChooseButton.js'

class Table extends Component {
  constructor(props) {
    super(props);
    this.state = {
      datas: [],   //setting data to empty at first
      called: [],
      pages: null,
      loading: true,
      callButton: 'Call',  //value of call button in the HTML
      result: ''
    };
  }

//Access-Control-Allow-Origin:
  getPatientsHandler = () => {
      $.ajax({
        type: 'POST',
        url: "http://0.0.0.0:8081/get_patient_data",  //mirroring python function, ajax call
        dataType: 'jsonp',
        contentType: 'application/json; charset=utf-8',
        success: function(data) {
         this.setState({datas: data['DATA']});  //grabs data and fills the rows with the ML trained data. 
       }.bind(this),
        error: function(error) {
          console.log(error)
        }
      })
    }

  sendAllPatients = () => {
    const { datas, pages, loading } = this.state;
    $.ajax({
      type: 'POST',
      url: "http://0.0.0.0:8081/load_newpatient_data",
      dataType: 'jsonp',
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify({'d': datas}),
      success: function(data) {
       alert(JSON.stringify(datas));
     }.bind(this),
      error: function(error) {
        console.log(datas)
      }
    })
  }

  sendCalledPatients = () => {
    const { datas, pages, loading } = this.state;
    $.ajax({
      type: 'POST',
      url: "http://0.0.0.0:8081/load_calledpatient_data",
      dataType: 'jsonp',
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify(this.state.called),
      success: function(data) {
       alert(JSON.stringify(data));
     }.bind(this),
      error: function(error) {
        console.log(error)
      }
    })
  }

  handleButtonClick = () => {
  }
  //function handles what to do when pop up comes up with whether or not they accpeted or rejected. 
  popUpHandler = (i) => {
    Popup.create({
   
    content: 'Please wait until call is completed before choosing response',
    buttons: {  //creating three buttons to accept, reject, or voicemail
        right: [{
            text: 'Enrolled',
            class: 'success',
            action: function () {
                this.setState({result:'ENROLLED'})
                $.ajax({
          type: 'POST',
          url: "http://0.0.0.0:8081/patient_stats",
          dataType: 'jsonp',
          contentType: 'application/json; charset=utf-8',
          data: {"id": i, "result": 'ENROLLED'}  //sending back the request data as a dict with the id as the id in the table
        })
                Popup.alert('Result of the call is saved successfully!');
                /** Close this popup. Close will always close the current visible one, if one is visible */
                Popup.close();
            }
        },{
            text: 'Rejected',
            id: 'danger',
            action: function () {
                this.setState({result:'REJECTED'})
                $.ajax({
          type: 'POST',
          url: "http://0.0.0.0:8081/patient_stats",
          dataType: 'jsonp',
          contentType: 'application/json; charset=utf-8',
          data: {"id": i, "result": 'REJECTED'}  //sending back the request data as a dict with the id as the id in the table
        })
                Popup.alert('Result of the call is saved successfully!');
                /** Close this popup. Close will always close the current visible one, if one is visible */
                Popup.close();
            }
        },{
            text: 'Voicemail',
            id: 'm',
            action: function () {
                this.setState({result:'VOICEMAIL'})
                $.ajax({
          type: 'POST',
          url: "http://0.0.0.0:8081/patient_stats",
          dataType: 'jsonp',
          contentType: 'application/json; charset=utf-8',
          data: {"id": i, "result": 'VOICEMAIL'}  //sending back the request data as a dict with the id as the id in the table
        })
                Popup.alert('Result of the call is saved successfully!');
                /** Close this popup. Close will always close the current visible one, if one is visible */
                Popup.close();
            }
        }]
    }
});
  }

  getTrProps = (state, rowInfo) => {
    return {
      onClick: e=> {
        if (document.getElementById("number").value == "Call"){
          //Popup.alert("Calling " + rowInfo.original.firstname + " " + rowInfo.original.lastname)
          this.popUpHandler(rowInfo.original.id)  //takes in the persons id as an argument
          const { datas, pages, loading } = this.state;
        $.ajax({
          type: 'POST',
          url: "http://0.0.0.0:8081/call_patient",
          dataType: 'jsonp',
          contentType: 'application/json; charset=utf-8',
          data: {"phone": rowInfo.original.phone},  //sends back phone number to know which person and # to call
          success: function(data) {
           console.log("called")
         }.bind(this),
          error: function(error) {
            console.log(rowInfo.original.id)
            var a = [...datas]
            a.splice(rowInfo.index, 1)  //after agent presses call button, removes row from the data table
            this.setState({datas: a})
          }.bind(this),
          async: false
        })
        }
     
      }
    }
  }


  render() {

  //const {data} = this.state;
  const { datas, pages, loading } = this.state;
  const style = {
      backgroundColor: 'white',
      font: 'inherit',
      border: '1px solid blue',
      padding: '8px',
      cursor: 'pointer'
    };


    //console.log(datas)
    return (
      <div>
      <Popup />
      <button
            style={style}
            onClick={() => this.getPatientsHandler()}>Get Patients</button>

        <ReactTable
          data={this.state.datas}
          columns = {[{
            Header: 'First Name',
            accessor: 'firstname' // String-based value accessors!
          }, {
            Header: 'Last Name',
            accessor: 'lastname'
          }, {
            Header: 'ID',
            accessor: 'id',
            Cell: props => <span className='number'>{props.value}</span> // Custom cell components!
          }, {
            Header: 'dob',
            accessor: 'dob'
          }, {
            Header: 'Phone Number',
            accessor: 'phone' // String-based value accessors!
          },{
            Header: 'Primary_payer',
            accessor: 'primary_payer' // String-based value accessors!
          },{
            Header: 'Medicare',
            accessor: 'medicare' // String-based value accessors!
          },{
            Header: 'hba',
            accessor: 'hba1c', // String-based value accessors!
            Cell: props => <span className='number'>{props.value}</span> // Custom cell components!
          },{
            Header: 'Timezone',
            accessor: 'timezone'
          }, {
            Header: 'Call',
            id: 'click-me-button',
            accessor: 'but',
            Cell: ({value}) => <input type="button" id='number' value="Call" onClick={(e) => this.handleButtonClick(e, value)} ></input>
          }]}
          manual// Forces table not to paginate or sort automatically, so we can handle it server-side
          getTrProps={this.getTrProps}  //assigns props to function. 
        />
      </div>
    );
}
};

export default Table;
