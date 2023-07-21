import os
from InquirerPy import inquirer
from InquirerPy.validator import PathValidator
from typing import Union, List
import pandas as pd

class CLIArgs:
    def __init__(self) -> None:
        self.home_path = "~/" if os.name == "posix" else "C:\\"

    def input_file_type(self) -> str:
        file_type = inquirer.select(
            message = "File Type: ",
            choices = [
                "csv",
                "json",
                "parquet",
                "excel"
            ],
            default = "csv"
        ).execute()
        return file_type

    def file_path(self) -> str:
        src_path = inquirer.filepath(
            message = "Enter File Path: ",
            default = self.home_path,
            validate = PathValidator(is_file = True, message = "input argument is not a file"),
            raise_keyboard_interrupt=False,
            mandatory_message="Prompt is mandatory, terminate the program using ctrl-d",
        ).execute()
        return src_path
    
    def output_path(self) -> str:
        output_path = inquirer.filepath(
            message = "Enter Output Path: ",
            default = self.home_path,
            validate = PathValidator(is_dir = True, message = "not a directory"),
            only_directories = True
        ).execute()
        return output_path
    
    def eda_type(self, cols:List[str]) -> Union[str, bool, pd.DataFrame]:
        eda_type = inquirer.select(
            message = "Select EDA Type: ",
            choices = ["Dataset Analysis", "Target Analysis", "Compare"],
            raise_keyboard_interrupt=False,
            mandatory_message="Prompt is mandatory, terminate the program using ctrl-d"
        ).execute()
        target = None
        test_df = None
        if eda_type == "Target Analysis" or eda_type == "Compare":
            target = inquirer.select(
                message = "Select Target Name: ",
                choices = cols,
                raise_keyboard_interrupt=False,
                mandatory_message="Prompt is mandatory, terminate the program using ctrl-d"
            ).execute()
        if eda_type == "Compare":
            test_df = inquirer.filepath(
                message = "Enter File Path: ",
                default = self.home_path,
                validate = PathValidator(is_file = True, message = "input argument is not a file"),
                raise_keyboard_interrupt=False,
                mandatory_message="Prompt is mandatory, terminate the program using ctrl-d",
                ).execute()
        return eda_type, target, test_df
