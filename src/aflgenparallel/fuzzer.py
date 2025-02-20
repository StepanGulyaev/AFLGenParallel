from pydantic import BaseModel, Field, model_validator

class Fuzzer(BaseModel):
    name: str = Field(..., min_length=1)
    number: Optional[int] = Field(None, gt=0)
    percentage: Optional[float] = Field(None, gt=0, le=1)

    @model_validator(mode="after")
    @classmethod
    def validate_xor_num_percentage(cls, values):
        if bool(values.number) ^ bool(values.percentage):
            raise ValueError("You have to use either number or percentage, but not both.")
        return values

    fuzzer_settings: FuzzerSettings = Field(...)

class FuzzerSettings(BaseModel):
    env_variables: Optional[List[str]] = Field(default=None)

    @field_valdator("env_variables",mode="after")
    @classmethod
    def validate_env_variables(cls, env_var):
        if env_var == []: 
            raise ValueError("If you have no env_variables in fuzzer_settings then set field to null.\
                    It made this way to make config format more strict for us not to deal with two values that \
                    mean practically the same thing in our case.")
        elif any(not var.strip() for var in env_var):
            raise ValueError("env_variables must not contain any empty lines")
        return env_var

    program_name: str = Field(..., min_length=1)
    options: dict = Field(...)
    




#class options(BaseModel):

    


