from app import *

from .data_cache import DataHandle


class ServerHandler(BaseHTTPRequestHandler):
    post_data_scheme = ['table_name', 'uid', 'column_name', 'data']
    data_handle: DataHandle = DataHandle(  )
    def do_GET(self):
        request_query_map = self.get_url_query_map(  )
        path = self.get_path(  )

        if path == 'data':
            column = request_query_map['column'][0]
            table = request_query_map['table'][0]

            data = self.data_handle.get_column_as_list( table_name=table, column_name=column )
            bytes = json.dumps({
                'data': data
            }).encode()
            self.end_response_and_headers(  )
            self.wfile.write( bytes )
        # /train?table=name        
        elif path == 'train':
            table_name,= request_query_map['table']
            ncomps,= request_query_map.get('nc', ('auto', ))
            if ncomps != 'auto':
                ncomps = int(ncomps)
            if self.data_handle.has_table( table_name=table_name ):
                self.data_handle.fit_table_store( table_name=table_name, n_components=ncomps )

                self.end_response_and_headers(  )
            else:
                self.end_response_and_headers(msg=F'no table with name {table_name}!')
        elif path == 'query':
            table_name ,= request_query_map['table']
            query_str ,= request_query_map['q']
            nresults, = request_query_map.get('nresults', (5, ))
            columns, = request_query_map.get('columns', (None, ))
            if not(columns is None):
                columns = [*map( lambda a:a.strip(' '), columns.split(',') )]
                
            print(f'{columns = }')
            nresults = int(nresults)

            if self.data_handle.has_table( table_name=table_name ):
                if self.data_handle.is_table_store_fitted( table_name=table_name ):
                    uid_results, str_results = self.data_handle.query_table_store( query=query_str, 
                                                                                  table_name=table_name, first=nresults,
                                                                                   columns=columns )
                    self.end_response_and_headers()
                    self.wfile.write( 
                        json.dumps(
                            {
                                'text_results': str_results,
                                'uid_results': uid_results
                            }
                        ).encode()
                    )
                else:
                    self.end_response_and_headers(msg=F'{table_name} has no fitted model call /train?table={table_name} to fit the model') 
            else:
                self.end_response_and_headers( msg=F'no table name {table_name}' )
            pass
        elif path == 'dummy':
            self.end_response_and_headers()
            self.dummy_data_test()

    
    def end_response_and_headers(self, code=200, msg=''):
        self.send_response( code=code, message=msg )
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow all origins
        self.end_headers(  )
        
    def dummy_data_test(self):
        conn = sqlite3.connect("example.db")
        res = conn.execute( f'select * from products' )
        rows = []
        while not( (row:=res.fetchone()) is None ):
            rows.append( row[0] )
        self.wfile.write(json.dumps( rows ).encode())

    def get_path(self):
        return parse.urlparse( self.stripped_path(  ) ).path

    def get_url_query_map(self):
        return parse.parse_qs(parse.urlparse( self.stripped_path(  ) ).query)

    '''
    send 
    {
        table_name: '',
        uid: '',
        column_name: '',
        column_data: []
    }
    '''
    def get_parsed_body(self):
        pass 
    def stripped_path(self):
        return self.path.strip('/')
    def do_POST(self):
        print(f'{self.path = }')
        byte_size = int( self.headers.get('content-length') )
        body = self.rfile.read( byte_size )
        parsed_data = json.loads( body )
        url_path = self.get_path(  )
        print(url_path)
        if url_path == 'column':
            if all( key in parsed_data for key in self.post_data_scheme ):
                self.end_response_and_headers(  )
                self.data_handle.push_column( 
                    **{
                        key: parsed_data[key] for key in self.post_data_scheme
                    }
                )
            else:
                self.end_response_and_headers( msg=F'Must follow scheme { self.post_data_scheme }' )


        

    

def run(handler_class=ServerHandler, port=8004):
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


