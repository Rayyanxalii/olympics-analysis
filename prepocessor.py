import pandas as pd



def preprocess(ath,reg):
    
    ath = ath[ath['Season'] == 'Summer']
    
    ath = ath.merge(reg, on='NOC', how='left')
    
    ath.drop_duplicates(inplace=True)
    
    ath = pd.concat ([ath,pd.get_dummies(ath['Medal'])],axis=1)
    return ath