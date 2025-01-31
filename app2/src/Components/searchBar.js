import { useState } from "react"

export default function SearchBar({onSearch}){
    let [query, setQuery] = useState( "" )
    
    async function handleSubmit(e) {
        e.preventDefault()
        console.log("submitting")
        let inr = parseInt(document.getElementById("nr").value)
        console.log("log afeter onSearch called")
        let res = await fetch(`http://localhost:8004/query?q=${
            new URLSearchParams({
            q: query,
            table: 'products',
            nresults: inr
            }).toString()
        }`).then(
            (res) => {
            return res.json()
            }
        )
        onSearch( res.text_results )
    }

    return <form className="form boder-green m-5" onSubmit={handleSubmit}>
            <label style={{color: 'red'}}  className="form-label">query</label>
            <input value={query} onChange={ (e) => {
                setQuery(e.target.value)
                console.log(query)
            } } type="text" itemID="inputPassword5" className="form-control" aria-describedby="passwordHelpBlock" />
            <div>
            <button className="btn btn-success mt-2">search</button>
            <input type='number' className="form-control" placeholder="num results" id="nr"></input>
            </div>
            <div itemID="passwordHelpBlock" className="form-text">
            .......
            </div>
    </form>
}