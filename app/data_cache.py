from app import *

class DataHandle:
    instance : 'DataHandle' 
    datastores : dict[str, 'TableDataStore'] = {}
    def __init__(self):
        pass

    def get_column_as_list( self, table_name, column_name ):
        ds = self.datastores.get( table_name, None )
        if ds is None:
            return []
        return  ds.columns[ column_name ].to_list()

    def get_column_as_numpy( self, table_name, column_name ):
        ds = self.datastores.get( table_name, None )
        if ds is None:
            return []
        return  ds.columns[ column_name ].to_numpy()

    def push_column(self, table_name, column_name: str, uid: list[str], data: list[str]):
        ds = self.datastores.get( table_name, None )
        if ds is None:
            ds = TableDataStore( table_name=table_name )
            self.datastores[ table_name ] = ds 
        ds.append_data_column( column_name=column_name, data=data )
        if not(uid is None):
            ds.set_column_uids( uids=uid ) 
        return ds 
    
    def query_table_store( self, query: str, table_name: str, first=5, res_fmt: str = 'list', columns=None ):
        ds = self.datastores.get( table_name, None )
        if  ds is None:
            return None 
        if not ds.is_model_fitted(): #RED
            ds.fit_data_model(  )
        uids, rdata = ds.rank_query( query=query, numpy=res_fmt=='numpy', _list=res_fmt=='list', columns=columns )
        N = len(rdata)
        print(f'{N = }, {first = }')
        nresults = min( N, first )
        return uids and uids[:nresults], rdata[:nresults]
    
    def is_table_store_fitted(self, table_name: str):
        return self.get_table_store( table_name=table_name ).is_model_fitted()
    
    def has_table(self, table_name: str):
        return table_name in self.datastores
    def get_table_store(self, table_name):
        return self.datastores.get( table_name, None )
    
    def fit_table_store(self, table_name, n_components):
        ds = self.get_table_store( table_name=table_name ) 
        ds.fit_data_model( n_components=n_components )   
        return True #RED
    
    def __str__(self):
        return '<empty>' #SHOW ds NAMES
    def __new__(cls):
        return quicksingleton( cls )
    

class TableDataStore:
    UID_COL_NAME: str = 'uid'
    columns: pd.DataFrame
    uid: pd.DataFrame
    model: LSAModel
    table_name: str
    def __init__(self, table_name = '(<)'):
        self.columns = pd.DataFrame(  )
        self.data_model = LSAModel(  )
        self.uid = pd.DataFrame( )
        self.table_name = table_name

    def append_data_column(self, column_name, data):
        self.columns[column_name] = data 
        print(self.columns[ column_name ])

    
    def set_column_uids(self, uids):
        self.uid[ self.UID_COL_NAME ] = uids
        print(self.uid)

    def is_model_fitted(self):
        return self.data_model.fitted

    def set_raw_column_uid(self, column_name, raw_uids):
        if column_name not in self.columns.columns:
            print("data must be inserted first")
            raise Exception()
        uids = json.loads( raw_uids )
        self.uid[ self.UID_COL_NAME ] = uids 

    def append_raw_data_column(self, column_name, raw_data):
        data_array = json.loads( raw_data )
        if not isinstance( data_array, list ):
            raise Exception( f"Invalid Type expected: {'list'}, got {type(data_array)}" )
        self.columns[ column_name ] = data_array
    
    def fit_data_model(self, columns: (str | list[str] ) ='all', n_components='auto'):
        if isinstance( columns, list ):
            raise NotImplementedError()
        if columns == 'all':
            text_data = self.columns.apply( lambda row: ', '.join(row.values.astype(str)), axis=1 ) 
        elif columns == 'first':
            raise NotImplementedError()
        self.data_model.num_components = n_components
        self.data_model.fit( text_data.to_numpy() )

    def rank_query(self, query: str, numpy=False, _list=False, columns=None):
        if not self.is_model_fitted(  ):
            raise Exception( "Model be fitted first" )
        ranks = self.data_model.rank_query( [ query ] )
        print(f'{ranks = }, {self.uid = }')
        if numpy:
            return self.columns.iloc[ ranks, : ].values
        elif _list == True:
            uids = None
            if len(self.uid.columns)==1:
                uids =  self.uid.iloc[ranks, :].values.flatten().tolist()
            if not(columns is None):
                print('not none', columns)
                cols = self.columns[columns].iloc[ ranks, : ].values.tolist() 
            else:
                cols = self.columns.iloc[ ranks, : ].values.flatten().tolist()
            return uids, cols
        else:
            return self.columns.iloc[ ranks, : ].to_list()

