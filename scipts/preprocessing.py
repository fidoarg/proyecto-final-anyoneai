import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin

class PerCatLimTransform(BaseEstimator, TransformerMixin):
    
    def __init__(self, percentage_limit: float, number_allowed_classes: int):
        
        assert 0 < percentage_limit < 1, 'precentage_limit needs to be between 0 and 1'
        assert isinstance(number_allowed_classes, int), 'number_allowed_classes needs to be an int'
        
        self.percentage_limit = percentage_limit
        self.number_allowed_classes= number_allowed_classes
        self.dict_accepted_values= {} 
        
    def fit(self, X, y= None):
        
        for col in X.columns:
            if isinstance(X[col].dtype, pd.CategoricalDtype):
                
                s= np.round(
                    X[col].value_counts(
                        normalize= True,
                        sort= True,
                        ascending= False,
                        dropna= False
                    )\
                        .cumsum(skipna= False),
                    decimals= 4
                )
                if len(s.index) < self.number_allowed_classes:
                    allowed_classes= s.index.to_list()
                else:
                    allowed_classes_per= list(s[s < self.percentage_limit].index)
                    last_value_index=s[s < self.percentage_limit].index[-1]
                    last_value= s[s < self.percentage_limit][-1]
                    
                    if not pd.isna(last_value) and allowed_classes_per.index(last_value_index) <= self.number_allowed_classes:
                        allowed_classes= allowed_classes_per
                    elif not pd.isna(last_value): 
                        allowed_classes= allowed_classes_per[:self.number_allowed_classes] 

                self.dict_accepted_values[col]= allowed_classes
                
            else:
                continue
                
        return self
        
    def transform(self, X):
        
        output_df= X.copy()
        
        for col in X.columns:
            if col in self.dict_accepted_values.keys():
                func= lambda value: 'OTRO' if not len(set(self.dict_accepted_values[col]) & set([value])) and not pd.isna(value) else value
                output_df.loc[:, col]= X.loc[:, col].apply(func)
        
        return output_df