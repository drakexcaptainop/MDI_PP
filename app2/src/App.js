import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import SearchBar from './Components/searchBar';
import Table from './Components/table';

const gData = [
  { id: 1, name: "asd1" },
  { id: 2, name: "asd2" },
  { id: 3, name: "asd3" },
  { id: 4, name: "asd4" },
]



function App() {
  let [filteredData, setFilteredData] = useState( gData )
  
  function handleSearch(query) {
    if(query == ""){
      setFilteredData( gData.slice() )
      return
    }
    let fd = gData.filter( v=>v.name.match( new RegExp( query ) )!==null )
    console.log( "fd", fd )
    setFilteredData( fd )
  }

  return (
    <div className="container" >
      <SearchBar 
        onSearch = {handleSearch}></SearchBar>
      <div className='container'>
        { filteredData.length == 0 ? <p style={{color: 'green'}}>No results found!</p> : <Table data = {filteredData}></Table> }
      </div>
    </div>
  );
}

export default App;
