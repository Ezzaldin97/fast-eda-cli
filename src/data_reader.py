import os
import pandas as pd
import numpy as np
from typing import Any
from InquirerPy import inquirer
from colors import Colors

colors = Colors()

class DataReader:

    @staticmethod
    def keep(col:str, col_dtype:str) -> Any:
        proceed = inquirer.confirm(message = f"keep {col} in dataset: ", default = True).execute()
        lst = None 
        if proceed:
            dtypes_lst = ['int8', 'int16', 'int32', 'int64', 'float8','float16','float32', 'float64', 'object']
            lst = inquirer.rawlist(
                message = f"Choose {col} Data-Type: ",
                choices = dtypes_lst,
                default = dtypes_lst.index(col_dtype)+1
            ).execute()
        return proceed, lst

    @staticmethod
    def reduce_memory_usage(df:pd.DataFrame) -> pd.DataFrame:
        numerics = ['int8', 'int16', 'int32', 'int64', 'float8','float16', 'float32', 'float64']
        start_mem = df.memory_usage().sum() / 1024**2    
        for col in df.columns:
            col_type = df[col].dtypes
            if col_type in numerics:
                c_min = df[col].min()
                c_max = df[col].max()
                if str(col_type)[:3] == 'int':
                    if (c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max) or (c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max):
                        df[col] = df[col].astype(np.int16)
                    elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                        df[col] = df[col].astype(np.int32)
                    elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                        df[col] = df[col].astype(np.int64)  
                else:
                    if (c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max) or (c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max):
                        df[col] = df[col].astype(np.float32)
                    else:
                        df[col] = df[col].astype(np.float64)    
        end_mem = df.memory_usage().sum() / 1024**2
        print(f'{colors.green}Mem. usage decreased to {end_mem:5.2f} Mb ({100 * (start_mem - end_mem) / start_mem:.1f}% reduction){colors.reset_colors}')
        return df
    
    @staticmethod
    def handle_duplicates(df:pd.DataFrame) -> pd.DataFrame:
        original = df.shape
        try:
            df.drop_duplicates(inplace=True, ignore_index=False)
            df = df.reset_index(drop=True)
            new = df.shape
            count = original[0] - new[0]
            print(f'{colors.green}Deletion of {count} duplicate(s) succeeded{colors.reset_colors}')
        except:
                print(f'{colors.red}Handling of duplicates failed{colors.reset_colors}')
        return df
    
    def read_data(self, data_path:str, file_format:str, test_data:bool=False) -> pd.DataFrame:
        if file_format == "csv":
            df = pd.read_csv(os.path.abspath(data_path), encoding_errors = "ignore")
        elif file_format == "json":
            df = pd.read_json(os.path.abspath(data_path), encoding_errors = "ignore")
        elif file_format == "parquet":
            df = pd.read_parquet(os.path.abspath(data_path))
        else:
            df = pd.read_excel(os.path.abspath(data_path), encoding_errors = "ignore")
        df = DataReader.reduce_memory_usage(df = df)
        df = DataReader.handle_duplicates(df = df)
        if not test_data:
            start_mem = df.memory_usage().sum() / 1024**2   
            for col in df.columns:
                col_type = df[col].dtype
                flag, col_dtype = DataReader.keep(col = col, col_dtype = col_type)
                if flag == False:
                    df.drop(col, axis = 1, inplace = True)
                else:
                    try:
                        df[col] = df[col].astype(col_dtype)
                    except:
                        print(f"{colors.red}Invalid Data-Type, Default Data-Type will be Applied{colors.reset_colors}")
            end_mem = df.memory_usage().sum() / 1024**2
            print(f'{colors.blue}Mem. usage decreased to {end_mem:5.2f} Mb ({100 * (start_mem - end_mem) / start_mem:.1f}% reduction){colors.reset_colors}')
        return df
