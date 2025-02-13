import argparse
import json
import os

def validate_config_file(path : str):
    try: 
        with open(path,"r",encoding="utf-8") as config:
            json.load(config)
    except json.JSONDecodeError as e:
        raise
    except FileNotFoundError as e
        raise

    return path

       
                
    return path

def parse_main_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f',
                        '--config-file',
                        type=validate_config_file, 
                        required=True, 
                        help="Config json file")
    parser.add_argument('-o',
                        '--output-file',
                        type=str, 
                        required=False,
                        default='AFLGenParallel_out.txt'
                        help="File with AFLGenParallel output")
    return parser.parse_args()


