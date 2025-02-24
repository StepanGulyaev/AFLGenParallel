import argparse
import json
import os

def validate_file(path : str):
    try: 
        file = open(path,"r",encoding="utf-8")
    except FileNotFoundError:
        raise
    return path


def parse_main_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f',
                        '--config-file',
                        type=validate_file, 
                        required=True, 
                        help="Config json file")
    parser.add_argument('-o',
                        '--output-file',
                        type=str, 
                        required=False,
                        default='aflgenparallel_out.txt',
                        help="File with AFLGenParallel output")
    return parser.parse_args()


