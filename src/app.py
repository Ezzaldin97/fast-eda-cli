from pyfiglet import Figlet
from args import CLIArgs
from validate_args import CustomValidator
from data_reader import DataReader
from eda import FastAnalyzer
import warnings

warnings.filterwarnings(action = "ignore")

if __name__ == "__main__":
    f = Figlet(font='slant')
    print(f.renderText('Fast EDA'))
    args = CLIArgs()
    file_type = args.input_file_type()
    file_path = args.file_path()
    validator = CustomValidator()
    validator.validate_input_path_type(file_path, file_type)
    report_path = args.output_path()
    reader = DataReader()
    df = reader.read_data(data_path = file_path,
                          file_format = file_type)
    eda_type, target, test_df_path = args.eda_type(list(df.columns))
    if test_df_path:
        test_df = reader.read_data(data_path = test_df_path,
                                   file_format = file_type,
                                   test_data = True)[df.columns]
    fast_analyzer = FastAnalyzer(df = df, output_path = report_path)
    fast_analyzer.analyze(eda_type = eda_type, test_df = test_df, target = target)