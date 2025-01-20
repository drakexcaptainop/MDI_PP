from app import *
from http.server import BaseHTTPRequestHandler, HTTPServer
from .data_cache import DataHandle

class ServerHandler(BaseHTTPRequestHandler):
    post_data_scheme = ['table_name', 'uid', 'column_name', 'data']
    data_handle: DataHandle = DataHandle(  )
    def do_GET(self):
        request_query_map = self.get_url_query_map(  )
        path = self.get_path(  )
        if path == 'data':
            column ,= request_query_map['column']
            table,= request_query_map['table']
            print(f'{request_query_map = }')
            data = self.data_handle.get_column_as_list( table_name=table, column_name=column )
            self.end_headers()
            bytes = json.dumps({
                'data': data
            }).encode()
            self.wfile.write( bytes )
            self.send_response(200)    
        self.end_headers()
        

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
        if url_path == 'column':
            if all( key in parsed_data for key in self.post_data_scheme ):
                self.send_response(200)
                self.end_headers()
                self.data_handle.push_column( 
                    **{
                        key: parsed_data[key] for key in self.post_data_scheme
                    }
                )
            else:
                self.send_response( 200, 'invalid scheme' )


        

    

def run(handler_class=ServerHandler, port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


