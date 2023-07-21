import os
import pandas as pd
import sweetviz as sv
from InquirerPy import inquirer
from colors import Colors

colors = Colors()

class FastAnalyzer:
    def __init__(self,
                 df:pd.DataFrame,
                 output_path:str) -> None:
        self.df = df
        self.output_path = output_path
    
    @staticmethod
    def enter_filename() -> str:
        filename = inquirer.text(
            message = "Enter HTML File Name: ",
            validate=lambda result: len(result) > 0,
            invalid_message="Input cannot be empty.",
            raise_keyboard_interrupt=False,
            mandatory_message="Prompt is mandatory, terminate the program using ctrl-d"
        ).execute()
        return filename

    def analyze(self,
                eda_type:str,
                test_df:pd.DataFrame=None,
                target:str=None) -> None:
        filename = FastAnalyzer.enter_filename()
        if eda_type == "Dataset Analysis":
            if self.df.shape[1] <= 10:
                analyze_report = sv.analyze(self.df)
            else:
                print(f"{colors.yellow}pairwise association will not be created due to large number of features{colors.reset_colors}")
                analyze_report = sv.analyze(self.df, pairwise_analysis = "off")
        elif eda_type == "Target Analysis":
            if self.df.shape[1] <= 10:
                analyze_report = sv.analyze(self.df, target_feat = target)
            else:
                print(f"{colors.yellow}pairwise association will not be created due to large number of features{colors.reset_colors}")
                analyze_report = sv.analyze(self.df, target_feat = target, pairwise_analysis = "off")
        elif eda_type == "Compare":
            if self.df.shape[1] <= 10:
                analyze_report = sv.compare(self.df, test_df, target)
            else:
                print(f"{colors.yellow}pairwise association will not be created due to large number of features{colors.reset_colors}")
                analyze_report = sv.compare(self.df, test_df, target, pairwise_analysis = "off")
        analyze_report.show_html(os.path.join(os.path.abspath(self.output_path), f"{filename}.html"),
                                 open_browser=False,
                                 layout = "vertical")