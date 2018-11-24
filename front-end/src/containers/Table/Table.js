import React, { Component } from 'react';
import ReactTable from 'react-table'
import 'react-table/react-table.css'
import $ from 'jquery';
//import {firstName} from '../../components/Button/ChooseButton.js'


class Table extends Component {
  constructor(props) {
    super(props);
    this.state = {
      datas: [],
      called: [],
      pages: null,
      loading: true
    };
  }

//Access-Control-Allow-Origin:
  getPatientsHandler = () => {
      $.ajax({
        type: 'POST',
        url: "http://0.0.0.0:8081/get_patient_data",
        dataType: 'jsonp',
        contentType: 'application/json; charset=utf-8',
        success: function(data) {
         this.setState({datas: data['DATA']});
       }.bind(this),
        error: function(error) {
          console.log(error)
        }
      })

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
    console.log(this.state.datas)
    return (
      <div>
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
          }]}
          manual// Forces table not to paginate or sort automatically, so we can handle it server-side
        />
      </div>
    );
}
};

export default Table;
