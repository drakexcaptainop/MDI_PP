export default function Table( { data } ){

    let keys = Object.keys( data[0] )
    return <table className="table table-dark table-borderless">
        <thead>
            <tr>
                { keys.map( (v, i) => <th key={i}> {v} </th>) }
            </tr>
        </thead>
        <tbody>
            { data.map( (v, i) => {
                return <tr> 
                    <th> { v.id } </th>  
                    <th> { v.name } </th>  
                </tr>
            } ) }
        </tbody>
    </table>


}