import React, { Component } from 'react';
import ReactTable from 'react-table'
import 'react-table/react-table.css'
//import {firstName} from '../../components/Button/ChooseButton.js'


/**const rawData = makeData();

const requestData = (pageSize, page, sorted, filtered) => {
  return new Promise((resolve, reject) => {
    // You can retrieve your data however you want, in this case, we will just use some local data.
    let filteredData = rawData;

    // You can use the filters in your request, but you are responsible for applying them.
    if (filtered.length) {
      filteredData = filtered.reduce((filteredSoFar, nextFilter) => {
        return filteredSoFar.filter(row => {
          return (row[nextFilter.id] + "").includes(nextFilter.value);
        });
      }, filteredData);
    }
    // You can also use the sorting in your request, but again, you are responsible for applying it.
    const sortedData = _.orderBy(
      filteredData,
      sorted.map(sort => {
        return row => {
          if (row[sort.id] === null || row[sort.id] === undefined) {
            return -Infinity;
          }
          return typeof row[sort.id] === "string"
            ? row[sort.id].toLowerCase()
            : row[sort.id];
        };
      }),
      sorted.map(d => (d.desc ? "desc" : "asc"))
    );

    // You must return an object containing the rows of the current page, and optionally the total pages number.
    const res = {
      rows: sortedData.slice(pageSize * page, pageSize * page + pageSize),
      pages: Math.ceil(filteredData.length / pageSize)
    };

    // Here we'll simulate a server response with 500ms of delay.
    setTimeout(() => resolve(res), 500);
  });
};

class Table extends Component {
  constructor(props) {
    super();
    this.state = {
      data: [],
      pages: null,
      loading: true
    };
    this.fetchData = this.fetchData.bind(this);
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
  /**const { data, pages, loading } = this.state;
    return (
      <div>
        <ReactTable
          columns = {[{
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
          }]}
          manual // Forces table not to paginate or sort automatically, so we can handle it server-side
          data={data}
          pages={pages} // Display the total number of pages
          loading={loading} // Display the loading overlay when we need it
          onFetchData={this.fetchData} // Request new data when things change
          filterable
          defaultPageSize={10}
          className="-striped -highlight"
        />
        <br />
        <Tips />
        <Logo />
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
        />
    </div>
  )*/
/**}
};*/

//export default Table;
