export default function Table( { data } ){

    let keys = Object.keys( data[0] )
    return <table className="table table-dark table-borderless">
        <thead>
            <tr>
                <th>Producto</th>
            </tr>
        </thead>
        <tbody>
            { data.map( (v, i) => {
                return <tr> 
                    <th> { v } </th>  
                </tr>
            } ) }
        </tbody>
    </table>


}