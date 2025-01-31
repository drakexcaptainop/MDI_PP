import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from 'react';
import SearchBar from './Components/searchBar';
import Table from './Components/table';

const gData = [
  { id: 1, name: "asd1" },
  { id: 2, name: "asd2" },
  { id: 3, name: "asd3" },
  { id: 4, name: "asd4" },
]


var Q;
function App() {
  let [filteredData, setFilteredData] = useState( null )
  console.log(`http://localhost:8004/query?${
      new URLSearchParams({
        q: Q,
        table: 'products',
        nresults: 10
      }).toString()
    }`)
  
  
  function handleSearch(data) {
      console.log(data)
      setFilteredData( data )
  }

  return (
    <div className="container" >
      <SearchBar 
        onSearch = {handleSearch}></SearchBar>
      <div className='container'>
        { filteredData?.length == 0 ? <p style={{color: 'green'}}>No results found!

        </p> : (filteredData && <Table data = {filteredData}></Table>) }
      </div>
    </div>
  );
}

export default App;
