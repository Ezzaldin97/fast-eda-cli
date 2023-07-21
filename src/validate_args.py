from prompt_toolkit.validation import ValidationError

class CustomValidator:
    
    def validate_input_path_type(self, input_path:str, type:str):
        input_path_type = input_path.split(".")[-1]
        if input_path_type != type:
            raise ValidationError(
                message="Input Data Type Doesn't Match File Type."
            )
