import os, sys
path_name= os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(path_name)

from _element import varr

import pandas as pd



defaultdirectory= varr.PJ_DIR + varr.DF_DIR

def from_xlsx(inputfilename, directory= defaultdirectory, inputsheetname= None):
    xls= pd.ExcelFile(directory+inputfilename)
    if not inputsheetname: inputsheetname= xls.sheet_names
    df_txs= pd.DataFrame()
    for sheet_name in inputsheetname:
        df= xls.parse(sheet_name)
        df_txs= pd.concat([df_txs, df])
    return df_txs

def to_xlsx(df, outputfilename, directory= defaultdirectory):
    writer= pd.ExcelWriter(directory+outputfilename, engine= 'xlsxwriter')
    df.to_excel(writer, sheet_name= outputfilename[:-5])
    writer.save()
    return None



def from_pickle(inputfilename, directory= defaultdirectory):
    return pd.read_pickle(directory+inputfilename)

def to_pickle(df, outputfilename, directory= defaultdirectory):
    df.to_pickle(directory+outputfilename)
    return None


def dir_list(data_path, ext):
    return [os.path.join(data_path, obj) for obj in os.listdir(data_path)\
            if os.path.splitext(obj)[-1]== ext]


    
# Main #########################################################################

if __name__== '__main__':
    pass
