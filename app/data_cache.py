from app import *


class DataHandle:
    instance : 'DataHandle' = None
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
        ds.set_column_uids( column_name=column_name, uids=uid ) 
        return ds 
    
    def query_table( self, query: str, table_name: str, first=5 ):
        ds = self.datastores.get( table_name, None )
        if  ds is None:
            return None 
        if not ds.is_model_fitted():
            ds.fit_data_model(  )
        [ruids, rdata] = ds.rank_query( query=query, numpy=True )
        N = ruids.shape[0]
        nresults = min( N, first )
        return ruids[:nresults], rdata[:nresults]

    def __str__(self):
        return '<empty>'
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__( cls )
        return cls.instance
    

class TableDataStore:
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
    
    def set_column_uids(self, column_name, uids):
        self.uid[ column_name ] = uids

    def is_model_fitted(self):
        return self.data_model.fitted

    def set_raw_column_uid(self, column_name, raw_uids):
        if column_name not in self.columns.columns:
            print("data must be inserted first")
            raise Exception()
        uids = json.loads( raw_uids )
        self.uid[ column_name ] = uids 

    def append_raw_data_column(self, column_name, raw_data):
        data_array = json.loads( raw_data )
        if not isinstance( data_array, list ):
            raise Exception( f"Invalid Type expected: {'list'}, got {type(data_array)}" )
        self.columns[ column_name ] = data_array
    
    def fit_data_model(self, columns: (str | list[str] ) ='all'):
        if isinstance( columns, list ):
            raise NotImplementedError()
        if columns == 'all':
            text_data = self.columns.apply( lambda row: ', '.join(row.values.astype(str)), axis=1 ) 
        elif columns == 'first':
            raise NotImplementedError()
        self.data_model.fit( text_data.to_numpy() )

    def rank_query(self, query: str, numpy=False):
        if not self.is_model_fitted(  ):
            raise Exception( "Model be fitted first" )
        ranks = self.data_model.rank_query( [ query ] )
        if numpy:
            return self.uid.iloc[ ranks ].to_numpy(), self.columns.iloc[ ranks, : ].to_numpy()
        else:
            return self.uid.iloc[ ranks ], self.columns.iloc[ ranks, : ]

