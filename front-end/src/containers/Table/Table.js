import React, { Component } from 'react';
import ReactTable from 'react-table'
import 'react-table/react-table.css'
import $ from 'jquery';
//import {firstName} from '../../components/Button/ChooseButton.js'


class Table extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      pages: null,
      loading: true
    }
  }
//Access-Control-Allow-Origin:
  getPatientsHandler = () => {
      $.ajax({
        type: 'POST',
        url: "http://0.0.0.0:8081/get_patient_data",
        dataType: 'jsonp',
        contentType: 'application/json; charset=utf-8',
        success: function(data) {
         this.setState({data: data.conversations});
         console.log(data)
       }.bind(this),
        error: function(error) {
          console.log(error)
        }
      })

    }
  render() {
    /**const data = [{
      name: firstName[8]
    }]*/
    /**const data = [{
        name: 'Tanner Linsley',
        age: 26,
        id:1,
        tz:'US/Central',
        intervention:'epxhyper',
        data:null,
        isAccepted:0,
        acceptedAt:null,
        isRejected:0,
        rejectedAt:null,
        hasContacted:1,
        lastContactedAt:'2018-09-04 15:58:56',
        patientId:1,
        phoneResourceId:1,
        createdAt:'2018-09-04 15:00:39',
        updatedAt:'2018-09-04 15:58:56',
        deletedAt:null,
      }]

      const columns = [{
        Header: 'Name',
        accessor: 'name' // String-based value accessors!
      }, {
        Header: 'Age',
        accessor: 'age',
        Cell: props => <span className='number'>{props.value}</span> // Custom cell components!
      }, {
        Header: 'Intervention',
        accessor: 'intervention' // String-based value accessors!
      },{
        Header: 'tz',
        accessor: 'tz' // String-based value accessors!
      },{
        Header: 'IsAccepted',
        accessor: 'isAccepted', // String-based value accessors!
        Cell: props => <span className='number'>{props.value}</span>
      },{
        Header: 'acceptedAt',
        accessor: 'acceptedAt'
      },{
        Header: 'isRejected',
        accessor: 'isRejected',
        Cell: props => <span className='number'>{props.value}</span>
      },{
        Header: 'rejectedAt',
        accessor: 'rejectedAt', // String-based value accessors!
      },{
        Header: 'hasContacted',
        accessor: 'hasContacted',
        Cell: props => <span className='number'>{props.value}</span>
      },{
        Header: 'lastContactedAt',
        accessor: 'lastContactedAt' // String-based value accessors!
      },{
        Header: 'patientId',
        accessor: 'patientId',
        Cell: props => <span className='number'>{props.value}</span>
      },{
        Header: 'phoneResourceId',
        accessor: 'phoneResourceId',
        Cell: props => <span className='number'>{props.value}</span>
      },{
        Header: 'createdAt',
        accessor: 'createdAt' // String-based value accessors!
      },{
        Header: 'updatedAt',
        accessor: 'updatedAt' // String-based value accessors!
      },{
        Header: 'deletedAt',
        accessor: 'deletedAt' // String-based value accessors!
      }]*/

  //const {data} = this.state;
  const { data, pages, loading } = this.state;
  const style = {
      backgroundColor: 'white',
      font: 'inherit',
      border: '1px solid blue',
      padding: '8px',
      cursor: 'pointer'
    };
    return (
      <div>
      <button
            style={style}
            onClick={() => this.getPatientsHandler()}>Get Patients</button>
        <ReactTable
          data={this.state.data}
          columns = {[{
            Header: 'First Name',
            accessor: 'firstname' // String-based value accessors!
          }]}
          manual // Forces table not to paginate or sort automatically, so we can handle it server-side
        />
      </div>
    );
  /**const columns = [{
    Header: 'Name',
    accessor: 'name' // String-based value accessors!
  }, {
    Header: 'Age',
    accessor: 'age',
    Cell: props => <span className='number'>{props.value}</span> // Custom cell components!
  }, {
    Header: 'Intervention',
    accessor: 'intervention' // String-based value accessors!
  },{
    Header: 'tz',
    accessor: 'tz' // String-based value accessors!
  }
  return(
    <div className = "Table">
      <ReactTable
        data={data}
        columns={columns}
        defaultPageSize={10}
        onFetchData={data}
        resolveData: data => resolvedData,
        />
    </div>
  )*/
}
};

export default Table;
