from app import *


def dummy():
    query = "4K LED Croma"
    pass

class LSAModel():
    fitted: bool = False
    svd_fit: TruncatedSVD
    vectorizer: TfidfVectorizer
    fitted_doc_matrix: np.ndarray
    num_components: ( int | str )
    def __init__(self, num_components: (int | str)='auto'):
        self.vectorizer = TfidfVectorizer(stop_words='english') 
        self.num_components = num_components

    def fit(self, text_data: list[str]):
        self.fitted = True
        X = self.vectorizer.fit_transform(text_data) 
        if self.num_components == 'auto':
            self.num_components = int(np.floor( np.sqrt( X.shape[0] ) ))
        self.svd_fit = TruncatedSVD(n_components=max(1, self.num_components)) 
        self.fitted_doc_matrix = self.svd_fit.fit_transform(X)
    

    def rank_query(self, query: list):
        vec_query = self.vectorizer.transform( query )
        reduced_query = self.svd_fit.transform( vec_query )
        corr = cosine_similarity( reduced_query, self.fitted_doc_matrix )
        sorted_ranks = corr.argsort()[0][::-1]
        return sorted_ranks

        