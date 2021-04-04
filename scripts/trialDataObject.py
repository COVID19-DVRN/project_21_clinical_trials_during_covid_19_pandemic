import pandas as pd

class trialDataObject:
    
    def __init__(self):
        self.dfs = []
    
    def addRow(self,
                study_id
                ,category,
                subcategory
                ,value
                ,title=[]
                ,design=[]
                ,group=[]
                

                ):
        
        
         df = pd.DataFrame(
                 columns=["study_id"

                          , "category",
                          "subcategory",
                          "value"
                         
                          ], 
                 index=range(1))
         
         df["study_id"] = study_id
         if len(title) > 0:
             df["title"] = title
         if len(design) > 0:
             df["type"] = design
         if len(group) > 0:
             df["group"] = group
         df["category"] = category
         df["subcategory"] = subcategory
         df["value"] = value
         self.dfs.append(df.copy())
                
         
    def getTrialData(self):
        return pd.concat(self.dfs)