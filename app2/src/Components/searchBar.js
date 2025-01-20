import { useState } from "react"

export default function SearchBar({onSearch}){
    let [query, setQuery] = useState( "" )

    function handleSubmit(e) {
        e.preventDefault()
        console.log("submitting")
        onSearch( query )
        console.log("log afeter onSearch called")
    }

    return <form className="form boder-green m-5" onSubmit={handleSubmit}>
            <label style={{color: 'red'}}  className="form-label">query</label>
            <input value={query} onChange={ (e) => {
                setQuery(e.target.value)
                console.log(query)
            } } type="text" itemID="inputPassword5" className="form-control" aria-describedby="passwordHelpBlock" />
            <button className="btn btn-success mt-2">search</button>
            <div itemID="passwordHelpBlock" className="form-text">
            .......
            </div>
    </form>
}