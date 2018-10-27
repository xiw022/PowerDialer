import React, { Component } from 'react';
import ReactTable from 'react-table'
import 'react-table/react-table.css'

class Table extends Component {
  constructor(props) {
    super(props);
    console.log("[Component.js] Inside Constructor", props);
    this.inputElement = React.createRef();
  }
  render () {
    const data = [{
        name: 'Tanner Linsley',
        age: 26,
        friend: {
          name: 'Jason Maurer',
          age: 23,
        },
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
        campaignId:1,
        phoneResourceId:1,
        createdAt:'2018-09-04 15:00:39',
        updatedAt:'2018-09-04 15:58:56',
        deletedAt:null,
      }]

      const columns = [{
        Header: 'Name',
        accessor: 'name' // String-based value accessors!
      }, {
        Header: 'Id',
        accessor: 'id',
        Cell: props => <span className='number'>{props.value}</span> // Custom cell components!
      }, {
        Header: 'tz',
        accessor: 'tz' // String-based value accessors!
      },{
        Header: 'Intervention',
        accessor: 'intervention' // String-based value accessors!
      },{
        Header: 'Data',
        accessor: 'data' // String-based value accessors!
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
        Header: 'campaignId',
        accessor: 'campaignId',
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
      }]


  return(
    <div className = "Table">
      <ReactTable
        data={data}
        columns={columns}
        />
    </div>
  )
}
};

export default Table;
