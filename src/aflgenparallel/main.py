import json
from aflgenparallel.cli import parse_main_args
from aflgenparallel.config_master import ConfigMaster

def execute_main():
    main_args = parse_main_args()
    
    config_master = ConfigMaster(main_args.config_file)
    

if __name__ == '__main__':
    execute_main()
