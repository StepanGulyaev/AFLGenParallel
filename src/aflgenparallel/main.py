import json
from aflgenparallel.cli import parse_main_args
from aflgenparallel.fuzzer import ConfigData

def execute_main():
    main_args = parse_main_args()
    
    with open(main_args.config_file,"r",encoding="utf-8") as config:
        try:
            config_data_raw = json.load(config)
        except json.JSONDecodeError as err:
            raise
    
    config_data = ConfigData.model_validate(config_data_raw)  
    config_data.print_parallel_fuzzing(main_args.output_file) 

if __name__ == '__main__':
    execute_main()
