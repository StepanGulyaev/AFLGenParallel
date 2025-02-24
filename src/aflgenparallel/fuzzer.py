from pydantic import BaseModel, Field, model_validator, field_validator
from typing import ForwardRef, Optional, Union, Any
import copy

Fuzzer = ForwardRef('Fuzzer')
FuzzerSettings = ForwardRef('FuzzerSettings')

class ConfigData(BaseModel):
    fuzzers: dict[str, Fuzzer]
    
    @field_validator("fuzzers",mode="after")
    @classmethod
    def check_fuzzers_exist(cls, fuzzers):
        if not fuzzers:
            raise ValueError("There has to be at least one fuzzer.")

        for fuzzer_name in fuzzers.keys():
            if not fuzzer_name.strip():
                raise ValueError("Fuzzer name must not be empty.")
        return fuzzers

    def print_parallel_fuzzing(self, output_file: str):
        records = []
        for fuzzer in self.fuzzers.values():
            for i in range(fuzzer.number):
                record = ""
                record += (" ".join(fuzzer.fuzzer_settings.env_variables) + " ")
                record += (fuzzer.fuzzer_settings.program_name + " ")

                options_copy = copy.deepcopy(fuzzer.fuzzer_settings.options)
                fuzzer_role = next(option for option in ("-M","-S") if option in options_copy)
                fuzzer_name = options_copy.pop(fuzzer_role)

                record += (" ".join(f"{key} {value}" for key, value in options_copy.items()) + " ")
                record += fuzzer_role + " "
                if i == 0: record += fuzzer_name + " "
                else: record += (fuzzer_name + str(i) + " ")

                record += fuzzer.fuzzer_settings.delimeter + " "
                record += fuzzer.fuzzer_settings.target + " "
                record += ((fuzzer.fuzzer_settings.target_args or "") + "\n")
                records.append(record)
        
        with open(output_file,"w") as file:
            file.writelines(records)

class Fuzzer(BaseModel):
    number: Optional[int] = Field(None, gt=0)
    fuzzer_settings: FuzzerSettings = Field(...)

class FuzzerSettings(BaseModel):
    env_variables: Optional[list[str]] = Field(default=None)

    @field_validator("env_variables",mode="after")
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
    options: dict[str, Union[str, Any]] = Field(...)
    
    @field_validator("options",mode="after")
    @classmethod
    def validate_options(cls, options):
        if not ( bool(options.get('-M')) ^ bool(options.get('-S'))):
                raise ValueError("Fuzzer have to be either master(-M) or slave(-S) but not both.")

        if not (options.get('-i')):
            raise ValueError("Input dir option is obligatory.")

        if not (options.get('-o')):
            raise ValueError("Output dir option is obligatory.")

        return options

    # Afl-fuzz requires you to have certain options, like -i and -o to run fuzzing, also it has certain datatypes for it's options.
    # But we are not going to check that in our program. Some options appear, some become deprecated. We want to maintain our utility 
    # as less as possible. AFLGenParallel allows you to pass wrong options through config, detecting these as error is up to AFL. 

    delimeter: Optional[str]
    target: str
    target_args: Optional[str]

#class options(BaseModel):

    


