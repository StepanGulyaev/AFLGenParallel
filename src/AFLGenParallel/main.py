import json
from AFLGenParallel.cli import parse_main_args


def execute_main():
    main_args = parse_main_args()

    with open(main_args.config_file,"r",encoding="utf-8") as config:
        config_data = json.load(config)
    #print(type(config_data))
    #print(config_data["fuzzers"]["master_fuzzer"])
    print(config_data)



if __name__ == '__main__':
    execute_main()
